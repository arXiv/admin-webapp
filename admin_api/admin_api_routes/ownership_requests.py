"""arXiv paper ownership routes."""

from datetime import datetime
from typing import Optional, Literal, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response

from sqlalchemy.orm import Session
from pydantic import BaseModel

from arxiv.base import logging
# from arxiv.db import transaction
from arxiv.db.models import OwnershipRequest

from . import is_admin_user, get_db
from .endorsement_requsets import EndorsementRequestModel
from .models import OwnershipRequestsAuditModel

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(is_admin_user)], prefix='/ownership_requests')

class PaperOwnerModel(BaseModel):
    class Config:
        orm_mode = True

    id: int # document_id
    user_id: int
    date: datetime
    added_by: int
    remote_addr: str
    remote_host: str
    tracking_cookie: str
    valid: bool
    flag_author: bool
    flag_auto: bool


class OwnershipRequestModel(BaseModel):
    class Config:
        orm_mode = True

    id: int  # request_id
    user_id: int
    endorsement_request_id: Optional[int] = None
    workflow_status: Literal['pending', 'accepted', 'rejected']
    request_audit: Optional[OwnershipRequestsAuditModel] = None
    endorsement_request: Optional[EndorsementRequestModel] = None

    @classmethod
    def base_query(cls, session: Session) -> Query:
        return session.query(
            OwnershipRequest.request_id.label("id"),
            OwnershipRequest.user_id,
            OwnershipRequest.endorsement_request_id,
            OwnershipRequest.workflow_status,
            OwnershipRequest.request_audit,
            OwnershipRequest.endorsement_request)


@router.get("/")
def list_ownership_requests(
        response: Response,
        _sort: Optional[str] = Query("last_name,first_name", description="sort by"),
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        user_id: Optional[int] = Query(None),
        endorsement_request_id: Optional[int] = Query(None),
        workflow_status: Optional[Literal['pending', 'accepted', 'rejected']] = Query(None),
        id: Optional[List[int]] = Query(None, description="List of user IDs to filter by"),
        session: Session = Depends(get_db),
    ) -> List[OwnershipRequestModel]:
    query = OwnershipRequestModel.base_query(session)
    if user_id:
        query = query.filter(OwnershipRequest.user_id == user_id)

    if id is not None:
        query = query.filter(OwnershipRequest.request_id.in_(id))

    if workflow_status is not None:
        query = query.filter(OwnershipRequest.workflow_status == workflow_status)

    if endorsement_request_id is not None:
        query = query.filter(OwnershipRequest.endorsement_request_id == endorsement_request_id)

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    result = [OwnershipRequestModel.from_orm(item) for item in query.offset(_start).limit(_end - _start).all()]
    return result
