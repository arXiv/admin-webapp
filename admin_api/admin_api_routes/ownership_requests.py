"""arXiv paper ownership routes."""
import re
import datetime
from enum import Enum
from typing import Optional, Literal, List

from arxiv.auth.user_claims import ArxivUserClaims
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response, Request
from sqlalchemy import insert

from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import and_
from pydantic import BaseModel

from arxiv.base import logging
from arxiv.db.models import OwnershipRequest, t_arXiv_ownership_requests_papers, PaperOwner, OwnershipRequestsAudit

from . import is_admin_user, get_db, is_any_user, get_current_user, transaction, datetime_to_epoch, VERY_OLDE
from .models import PaperOwnerModel

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(is_any_user)], prefix='/ownership_requests')


class WorkflowStatus(str, Enum):
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'


class OwnershipRequestModel(BaseModel):
    class Config:
        orm_mode = True

    id: int  # request_id
    user_id: int
    endorsement_request_id: Optional[int] = None
    workflow_status: WorkflowStatus # Literal['pending', 'accepted', 'rejected']
    date: Optional[datetime.date]
    document_ids: Optional[List[int]] = None

    @classmethod
    def base_query_0(cls, session: Session) -> Query:
        return session.query(
            OwnershipRequest.request_id.label("id"),
            OwnershipRequest.user_id,
            OwnershipRequest.endorsement_request_id,
            OwnershipRequest.workflow_status)

    @classmethod
    def base_query(cls, session: Session) -> Query:
        return session.query(
            OwnershipRequest.request_id.label("id"),
            OwnershipRequest.user_id,
            OwnershipRequest.endorsement_request_id,
            OwnershipRequest.workflow_status,
            OwnershipRequestsAudit.date
            ).join(
                OwnershipRequestsAudit, OwnershipRequest.request_id == OwnershipRequestsAudit.request_id
            )


    @classmethod
    def from_record(cls, record: OwnershipRequest, session: Session) -> 'OwnershipRequestModel':
        data: 'OwnershipRequestModel' = cls.from_orm(record)
        populate_document_ids(data, record, session)
        return data



def populate_document_ids(data: OwnershipRequestModel, record: OwnershipRequest, session: Session):
    data.document_ids = [
        requested.document_id for requested in session.query(
            t_arXiv_ownership_requests_papers.c.document_id
        ).filter(
            t_arXiv_ownership_requests_papers.c.request_id == data.id
        ).all()]


@router.get("/")
def list_ownership_requests(
        response: Response,
        _sort: Optional[str] = Query("last_name,first_name", description="sort by"),
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        preset: Optional[str] = Query(None),
        start_date: Optional[datetime.date] = Query(None, description="Start date for filtering"),
        end_date: Optional[datetime.date] = Query(None, description="End date for filtering"),
        id: Optional[List[int]] = Query(None, description="List of ownership request IDs to filter by"),
        user_id: Optional[int] = Query(None),
        endorsement_request_id: Optional[int] = Query(None),
        workflow_status: Optional[Literal['pending', 'accepted', 'rejected']] = Query(None),
        session: Session = Depends(get_db),

    ) -> List[OwnershipRequestModel]:
    query = OwnershipRequestModel.base_query(session)
    if id is not None:
        query = query.filter(OwnershipRequest.request_id.in_(id))
        _start = None
        _end = None
    else:
        if preset is not None or start_date is not None or end_date is not None:
            t0 = datetime.datetime.now(datetime.UTC)
            if preset is not None:
                matched = re.search(r"last_(\d+)_days", preset)
                if matched:
                    t_begin = datetime_to_epoch(None, t0 - datetime.timedelta(days=int(matched.group(1))))
                    t_end = datetime_to_epoch(None, t0)
                    query = query.filter(OwnershipRequestsAudit.date.between(t_begin, t_end))
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Invalid preset format")
            else:
                if start_date or end_date:
                    t_begin = datetime_to_epoch(start_date, VERY_OLDE)
                    t_end = datetime_to_epoch(end_date, datetime.date.today(), hour=23, minute=59, second=59)
                    query = query.filter(OwnershipRequestsAudit.date.between(t_begin, t_end))

        if user_id:
            query = query.filter(OwnershipRequest.user_id == user_id)

        if workflow_status is not None:
            query = query.filter(OwnershipRequest.workflow_status == workflow_status)

        if endorsement_request_id is not None:
            query = query.filter(OwnershipRequest.endorsement_request_id == endorsement_request_id)

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    result = [OwnershipRequestModel.from_record(item, session) for item in query.offset(_start).limit(_end - _start).all()]
    return result


@router.get("/{id:int}")
async def get_ownership_request(
        id: int,
        session: Session = Depends(get_db),
    ) ->OwnershipRequestModel:
    oreq = OwnershipRequestModel.base_query(session).filter(OwnershipRequest.request_id == id).one_or_none()
    if oreq is None:
        return Response(status_code=404)
    return OwnershipRequestModel.from_record(oreq, session)
    return oreq


@router.put('/{id:int}')
async def update_ownership_request(
        request: Request,
        id: int,
        current_user: ArxivUserClaims = Depends(get_current_user),
        session: Session = Depends(transaction)) -> OwnershipRequestModel:
    """Uptade ownership request.
{'flag_author_docid_NNNNN': True, 'document_ids': [2213327], 'endorsement_request_id': None, 'id': 54819, 'user_id': 499594, 'workflow_status': 'accepted'}

    """
    body = await request.json()
    row = session.query(OwnershipRequest).filter(OwnershipRequest.request_id == id).one_or_none()
    if row is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,)

    workflow_status = body.get('workflow_status', row.workflow_status)
    if workflow_status not in [ws.value for ws in WorkflowStatus]:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"workflow_status {workflow_status} is invalid")

    # ownreq = OwnershipRequest.from_record(row, session)
    user_id = row.user_id
    admin_id = current_user.user_id

    match workflow_status:
        case WorkflowStatus.accepted:
            doc_ids = body.get('document_ids', [])

            already_owns = session.query(PaperOwner.document_id).filter(and_(
                PaperOwner.user_id == user_id,
                PaperOwner.document_id.in_(doc_ids),
                PaperOwner.flag_author == 1)).all()

            accepting = set(doc_ids).remove(set([doc.document_id for doc in already_owns]))
            cookie_name = request.app.extra['settings'].config['CLASSIC_TRACKING_COOKIE']
            cookie = request.cookies.get(cookie_name)
            t_now = datetime.utcnow()
            for doc_id in accepting:
                marker = f"flag_author_doc_{doc_id}"
                if marker not in body:
                    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                         detail=f"flag_author_doc_{doc_id} is not in the body")
                value = body.get(marker)
                stmt = insert(PaperOwner).values(
                    document_id = doc_id,
                    user_id = user_id,
                    date = t_now,
                    added_by = admin_id,
                    remote_addr = request.client.host,
                    tracking_cookie = cookie,
                    flag_auto = 0,
                    flag_author = value)
                session.execute(stmt)
            pass

        case WorkflowStatus.rejected:
            pass

        case WorkflowStatus.pending:
            pass

    row.workflow_status = workflow_status
    session.commit()
    session.refresh(row)
    return OwnershipRequestModel.from_record(row, session)
