"""arXiv paper ownership routes."""

from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from arxiv.base import logging
from arxiv.db import get_db, transaction
from arxiv.db.models import Endorsement, EndorsementRequest, Demographic, TapirUser

from . import is_admin_user

logger = logging.getLogger(__name__)


router = APIRouter(dependencies=[Depends(is_admin_user)], prefix='/ownership')

@router.get("/")
def list_owners():
    # ownership_listing(workflow_status: str,
    #                      days_back: int) -> dict:
        report_stmt = (select(OwnershipRequest)
                       .options(joinedload(OwnershipRequest.user))
                       .filter(OwnershipRequest.workflow_status == workflow_status)
                       .limit(per_page).offset((page - 1) * per_page))
        count_stmt = (select(func.count(OwnershipRequest.request_id))
                      .where(OwnershipRequest.workflow_status == workflow_status))

        if workflow_status in ('accepted', 'rejected'):
            window = datetime.now() - timedelta(days=days_back)
            report_stmt = report_stmt.join(OwnershipRequestsAudit).filter(
                OwnershipRequestsAudit.date > window)
            count_stmt = count_stmt.join(OwnershipRequestsAudit).filter(
                OwnershipRequestsAudit.date > window)

        oreqs = session.scalars(report_stmt)
        count = session.execute(count_stmt).scalar_one()
        pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
        return dict(pagination=pagination, count=count, ownership_requests=oreqs,
                    worflow_status=workflow_status, days_back=days_back)


@router.get('/pending')
def pending() -> Response:
    """Pending ownership requests."""

    data = ownership_listing('pending', per_page, page, 0)
    data['title'] = "Ownership Reqeusts: Pending"
    return render_template('ownership/list.html',
                           **data)


@router.get('/accepted')
def accepted() -> Response:
    """Accepted ownership requests."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    days_back = args.get('days_back', default=7, type=int)

    data['title'] = f"Ownership Reqeusts: accepted last {days_back} days"
    return render_template('ownership/list.html',
                           **data)


@router.get('/rejected', methods=['GET'])
@admin_scoped
def rejected() -> Response:
    """Rejected ownership reqeusts."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    days_back = args.get('days_back', default=7, type=int)

    data = ownership_listing('rejected', per_page, page, days_back=days_back)
    data['title'] = f"Ownership Reqeusts: Rejected last {days_back} days"
    return render_template('ownership/list.html',
                           **data)

# @scoped()
@router.get('/need-paper-password', methods=['GET','POST'])
@admin_scoped
def need_papper_password() -> Response:
    """User claims ownership of a paper using submitter provided password."""
    form = PaperPasswordForm()
    if request.method == 'GET':
        return render_template('ownership/need_paper_password.html', **dict(form=form))
    elif request.method == 'POST':
        data=paper_password_post(form, request)
        if data['success']:
            return render_template('ownership/need_paper_password.html', **data)
        else:
            return make_response(render_template('ownership/need_paper_password.html', **data), 400)


@router.get('/{ownership_id:int}')
def ownership_detail(ownership_id:int, ) -> dict:
    """Display a ownership request.

    """
    stmt = (select(OwnershipRequest)
            .options(
                joinedload(OwnershipRequest.user).joinedload(TapirUser.tapir_nicknames),
                joinedload(OwnershipRequest.user).joinedload(TapirUser.owned_papers),
                joinedload(OwnershipRequest.request_audit),
                joinedload(OwnershipRequest.documents),
                joinedload(OwnershipRequest.endorsement_request).joinedload(EndorsementRequest.audit)
            )
            .where( OwnershipRequest.request_id == ownership_id))
    oreq = session.scalar(stmt)
    if not oreq:
        abort(404)

    already_owns =[paper.document.paper_id for paper in oreq.user.owned_papers]
    for paper in oreq.documents:
        setattr(paper, 'already_owns', paper.paper_id in already_owns)

    endorsement_req = oreq.endorsement_request if oreq.endorsement_request else None
    data = dict(ownership=oreq,
                user=oreq.user,
                nickname= oreq.user.tapir_nicknames.nickname,
                papers=oreq.documents,
                audit=oreq.request_audit,
                ownership_id=ownership_id,
                docids =  [paper.paper_id for paper in oreq.documents],
                endorsement_req=endorsement_req,)

    if postfn:
        data=postfn(data)

    return data

@router.post('/{ownership_id:int}')
def ownership_detail(ownership_id:int, postfn=None) -> dict:
    """Display a ownership request.

    """
    stmt = (select(OwnershipRequest)
            .options(
                joinedload(OwnershipRequest.user).joinedload(TapirUser.tapir_nicknames),
                joinedload(OwnershipRequest.user).joinedload(TapirUser.owned_papers),
                joinedload(OwnershipRequest.request_audit),
                joinedload(OwnershipRequest.documents),
                joinedload(OwnershipRequest.endorsement_request).joinedload(EndorsementRequest.audit)
            )
            .where( OwnershipRequest.request_id == ownership_id))
    oreq = session.scalar(stmt)
    if not oreq:
        abort(404)

    already_owns =[paper.document.paper_id for paper in oreq.user.owned_papers]
    for paper in oreq.documents:
        setattr(paper, 'already_owns', paper.paper_id in already_owns)

    endorsement_req = oreq.endorsement_request if oreq.endorsement_request else None
    data = dict(ownership=oreq,
                user=oreq.user,
                nickname= oreq.user.tapir_nicknames.nickname,
                papers=oreq.documents,
                audit=oreq.request_audit,
                ownership_id=ownership_id,
                docids =  [paper.paper_id for paper in oreq.documents],
                endorsement_req=endorsement_req,)

    if postfn:
        data=postfn(data)

    return data
