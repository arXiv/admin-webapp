"""arXiv ownership routes."""
from datetime import timedelta, datetime, date
from typing import Optional, List
import re

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Response

from sqlalchemy import select, update, func, case, Select, distinct, exists, and_, alias
from sqlalchemy.orm import Session, joinedload

from pydantic import BaseModel, validator
from arxiv.base import logging
from arxiv.db import transaction
from arxiv.db.models import PaperOwner

from . import is_admin_user, get_db, datetime_to_epoch, VERY_OLDE


logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(is_admin_user)], prefix="/ownerships")


class OwnershipModel(BaseModel):
    class Config:
        orm_mode = True

    document_id: int
    user_id: int
    date: datetime
    added_by: int
    remote_addr: str
    remote_host: str
    tracking_cookie: str
    valid: bool
    flag_author: bool
    flag_auto: bool

    @staticmethod
    def base_select(db: Session):
        return db.query(
            PaperOwner.document_id,
            PaperOwner.user_id,
            PaperOwner.date,
            PaperOwner.added_by,
            PaperOwner.remote_addr,
            PaperOwner.remote_host,
            PaperOwner.tracking_cookie,
            PaperOwner.valid,
            PaperOwner.flag_author,
            PaperOwner.flag_auto,
        )


@router.get('/')
async def list_ownerships(
        response: Response,
        _sort: Optional[str] = Query("issued_when", description="sort by"),
        _order: Optional[str] = Query("DESC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        preset: Optional[str] = Query(None),
        start_date: Optional[datetime] = Query(None, description="Start date for filtering"),
        end_date: Optional[datetime] = Query(None, description="End date for filtering"),
        flag_valid: Optional[bool] = Query(None),
        db: Session = Depends(get_db)
    ) -> List[OwnershipModel]:
    query = OwnershipModel.base_select(db)

    if _start < 0 or _end < _start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start or end index")

    t0 = datetime.now()

    order_columns = []
    if _sort:
        keys = _sort.split(",")
        for key in keys:
            if key == "id":
                key = "ownership_id"
            try:
                order_column = getattr(PaperOwner, key)
                order_columns.append(order_column)
            except AttributeError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid start or end index")

    if preset is not None:
        matched = re.search("last_(\d+)_days", preset)
        if matched:
            t_begin = datetime_to_epoch(None, t0 - timedelta(days=int(matched.group(1))))
            t_end = datetime_to_epoch(None, t0)
            query = query.filter(PaperOwner.issued_when.between(t_begin, t_end))
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid preset format")
    else:
        if start_date or end_date:
            t_begin = datetime_to_epoch(start_date, VERY_OLDE)
            t_end = datetime_to_epoch(end_date, date.today(), hour=23, minute=59, second=59)
            query = query.filter(PaperOwner.issued_when.between(t_begin, t_end))

    if flag_valid is not None:
        query = query.filter(PaperOwner.flag_valid == flag_valid)

    for column in order_columns:
        if _order == "DESC":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())


    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    result = [OwnershipModel.from_orm(item) for item in query.offset(_start).limit(_end - _start).all()]
    return result


@router.get('/{id:int}')
async def get_ownership(id: int, db: Session = Depends(get_db)) -> OwnershipModel:
    item = OwnershipModel.base_select(db).filter(PaperOwner.ownership_id == id).all()
    if item:
        return OwnershipModel.from_orm(item[0])
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id:int}')
async def update_ownership(
        request: Request,
        id: int,
        session: Session = Depends(transaction)) -> OwnershipModel:
    body = await request.json()

    item = session.query(PaperOwner).filter(PaperOwner.ownership_id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify?
    for key, value in body.items():
        if key in item.__dict__:
            setattr(item, key, value)

    session.commit()
    session.refresh(item)  # Refresh the instance with the updated data
    return OwnershipModel.from_orm(item)


@router.post('/')
async def create_ownership(
        request: Request,
        session: Session = Depends(transaction)) -> OwnershipModel:
    body = await request.json()

    item = PaperOwner(**body)
    session.add(item)
    session.commit()
    session.refresh(item)
    return OwnershipModel.from_orm(item)
