"""arXiv endorsement routes."""
import re
from datetime import timedelta, datetime, date
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Response

from sqlalchemy import select, update, func, case, Select, distinct, exists, and_
from sqlalchemy.orm import Session, joinedload

from pydantic import BaseModel
from arxiv.base import logging
from arxiv.db import transaction
from arxiv.db.models import Endorsement, EndorsementRequest, Demographic, TapirUser, Category, \
    EndorsementRequestsAudit

from . import is_admin_user, get_db, datetime_to_epoch, VERY_OLDE, CategoryModel

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(is_admin_user)], prefix="/endorsement_requests")


class EndorsementRequestModel(BaseModel):
    class Config:
        orm_mode = True

    id: int
    endorsee_id: int
    archive: str
    subject_class: str
    # secret: str
    flag_valid: bool
    issued_when: datetime
    point_value: int
    flag_suspect: bool

    arXiv_categories: Optional[CategoryModel]
    # arXiv_categories = relationship('Category', primaryjoin='and_(EndorsementRequest.archive == Category.archive, EndorsementRequest.subject_class == Category.subject_class)', back_populates='arXiv_endorsement_requests')

    # endorsee: list[UserModel]
    # endorsee = relationship('TapirUser', primaryjoin='EndorsementRequest.endorsee_id == TapirUser.user_id', back_populates='arXiv_endorsement_requests', uselist=False)

    # endorsement: list[EndorsementModel]
    # endorsement = relationship('Endorsement', back_populates='request', uselist=False)

    # audit: list[OwnershipRequestsAuditModel]
    # audit = relationship('EndorsementRequestsAudit', uselist=False)

    #@validator('issued_when', pre=True)
    #def convert_epoch_to_date(cls, v):
    #    # Assuming the incoming value `v` is a Unix epoch time as an int
    #    return datetime.fromtimestamp(v) if isinstance(v, int) else v

    @staticmethod
    def base_select(db: Session):

        return db.query(
            EndorsementRequest.request_id.label("id"),
            EndorsementRequest.endorsee_id,
            EndorsementRequest.archive,
            EndorsementRequest.subject_class,
            EndorsementRequest.flag_valid,
            EndorsementRequest.issued_when,
            EndorsementRequest.point_value,
            Demographic.flag_suspect.label("flag_suspect"),

            Category,
            # Endorsee ID (single value)
            #TapirUser.user_id.label("endorsee"),
            # Endorsement ID (single value)
            #Endorsement.endorsement_id.label("endorsement"),
            # Audit ID (single value)
            #EndorsementRequestsAudit.session_id.label("audit")
        ).outerjoin(
            Category,
            and_(
                EndorsementRequest.archive == Category.archive,
                EndorsementRequest.subject_class == Category.subject_class
            )
        ).outerjoin(
            Demographic,
            and_(
                Demographic.user_id == EndorsementRequest.endorsee_id,
            )
        )
    pass



@router.get('/')
async def list_endorsement_requests(
        response: Response,
        _sort: Optional[str] = Query("id", description="sort by"),
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        preset: Optional[str] = Query(None),
        start_date: Optional[date] = Query(None, description="Start date for filtering"),
        end_date: Optional[date] = Query(None, description="End date for filtering"),
        flag_valid: Optional[bool] = Query(None),
        not_positive: Optional[bool] = Query(None, description="Not positive point value"),
        suspected: Optional[bool] = Query(None, description="Suspected user"),
        db: Session = Depends(get_db)
    ) -> List[EndorsementRequestModel]:
    query = EndorsementRequestModel.base_select(db)

    if _start < 0 or _end < _start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start or end index")

    order_columns = []
    if _sort:
        keys = _sort.split(",")
        for key in keys:
            if key == "id":
                key = "request_id"
            try:
                order_column = getattr(EndorsementRequest, key)
                order_columns.append(order_column)
            except AttributeError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid start or end index")

    t0 = datetime.now()

    if preset is not None:
        matched = re.search("last_(\d+)_days", preset)
        if matched:
            t_begin = datetime_to_epoch(None, t0 - timedelta(days=int(matched.group(1))))
            t_end = datetime_to_epoch(None, t0)
            query = query.filter(EndorsementRequest.issued_when.between(t_begin, t_end))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid preset format")
    else:
        if start_date or end_date:
            t_begin = datetime_to_epoch(start_date, VERY_OLDE)
            t_end = datetime_to_epoch(end_date, date.today(), hour=23, minute=59, second=59)
            query = query.filter(EndorsementRequest.issued_when.between(t_begin, t_end))

    if flag_valid is not None:
        query = query.filter(EndorsementRequest.flag_valid == flag_valid)

    for column in order_columns:
        if _order == "DESC":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    if not_positive is not None:
        if not_positive:
            query = query.filter(EndorsementRequest.point_value <= 0)
        else:
            query = query.filter(EndorsementRequest.point_value > 0)

    if suspected is not None:
        query = query.join(Demographic, Demographic.user_id == EndorsementRequest.endorsee_id)
        query = query.filter(Demographic.flag_suspect == suspected)

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    result = [EndorsementRequestModel.from_orm(item) for item in query.offset(_start).limit(_end - _start).all()]
    return result


@router.get('/{id:int}')
async def get_endorsement_request(id: int, db: Session = Depends(get_db)) -> EndorsementRequestModel:
    item = EndorsementRequestModel.base_select(db).filter(EndorsementRequest.request_id == id).all()
    if item:
        return EndorsementRequestModel.from_orm(item[0])
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id:int}')
async def update_endorsement_request(
        request: Request,
        id: int,
        session: Session = Depends(transaction)) -> EndorsementRequestModel:
    body = await request.json()

    item = session.query(EndorsementRequest).filter(EndorsementRequest.request_id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify?
    for key, value in body.items():
        if key in item.__dict__:
            setattr(item, key, value)

    session.commit()
    session.refresh(item)  # Refresh the instance with the updated data
    return EndorsementRequestModel.from_orm(item)


@router.post('/')
async def create_endorsement_request(
        request: Request,
        session: Session = Depends(transaction)) -> EndorsementRequestModel:
    body = await request.json()

    item = EndorsementRequest(**body)
    session.add(item)
    session.commit()
    session.refresh(item)
    return EndorsementRequestModel.from_orm(item)


@router.delete('/{id:int}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_endorsement_request(
        id: int,
        session: Session = Depends(transaction)) -> Response:

    item = session.query(EndorsementRequest).filter(EndorsementRequest.request_id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")

    item.delete_instance()
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
