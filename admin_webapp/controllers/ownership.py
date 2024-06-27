"""arXiv paper ownership controllers."""

from datetime import datetime, timedelta
from pytz import timezone
import logging

from flask import Blueprint, request, current_app, Response, abort

from sqlalchemy import Integer, String, select, func, text, insert, update
from sqlalchemy.orm import joinedload
from arxiv.base import logging
from sqlalchemy.exc import IntegrityError

from arxiv.auth.auth.decorators import scoped
from arxiv.db import session
from arxiv.db.models import OwnershipRequest, OwnershipRequestsAudit, TapirUser, EndorsementRequest, PaperOwner

from .util import Pagination

logger = logging.getLogger(__file__)

blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')


def ownership_post(data:dict) -> Response:
    """Edit a ownership request.

    On reject, it should set the ownership as "rejected".

    On revisit is should set the ownership as "pending".

    Otherwise,
    it should make a list of all ids from the form that are checked,
    check they are not already owned,
    set the values in arXiv_paper_owners,
    set a row in admin_log with "add-paper-owner-2"

    See tapir/site-src/admin/code/process-ownership-head.php.m4

    Note: This doesn't do "bulk" mode
    """
    oreq = data['ownership']
    if request.method == 'POST':
        admin_id = 1234 #request.auth.user.user_id
        if 'make_owner' in request.form:
            already_owns = set([doc.document_id for doc in oreq.user.owned_papers])
            docs_to_own = set([ int(key.split('_')[1]) for key, _ in request.form.items()
                            if key.startswith('approve_')])
            to_add_ownership = docs_to_own - already_owns

            is_author = 1 if request.form['is_author'] else 0
            cookie = request.cookies.get(current_app.config['CLASSIC_TRACKING_COOKIE'])
            now = int(datetime.now().astimezone(timezone(current_app.config['ARXIV_BUSINESS_TZ'])).timestamp())

            for doc_id in to_add_ownership:
                session.add(PaperOwner(
                    document_id=doc_id, user_id=oreq.user.user_id, date=now,
                    added_by=admin_id, remote_addr=request.remote_addr, tracking_cookie=cookie,
                    flag_auto=0, flag_author=is_author))
                #audit_admin(oreq.user_id, 'add-paper-owner-2', doc_id)

            oreq.workflow_status = 'accepted'
            session.execute(update(OwnershipRequest)
                            .where(OwnershipRequest.request_id == oreq.request_id)
                            .values(workflow_status = 'accepted'))

            data['success']='accepted'
            data['success_count'] = len(docs_to_own - already_owns)
            data['success_already_owned'] = len(docs_to_own & already_owns)
        elif 'reject' in request.form:
            stmt = (
                update(OwnershipRequest)
                .where(OwnershipRequest.request_id == oreq.request_id)
                .values(workflow_status = 'rejected')
            )
            session.execute(stmt)
            data['success']='rejected'
        elif 'revisit' in request.form:
            # A revisit does not undo the paper ownership. This the same as legacy.
            stmt = (
                update(OwnershipRequest)
                .where(OwnershipRequest.request_id == oreq.request_id)
                .values(workflow_status = 'pending')
            )
            session.execute(stmt)
            data['success']='revisited'
        else:
            abort(400)

    session.commit()
    return data


@blueprint.route('/<int:ownership_id>', methods=['GET', 'POST'])
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

def ownership_listing(workflow_status:str, per_page:int, page: int,
                       days_back:int) -> dict:
    report_stmt = (select(OwnershipRequest)
                   .options(joinedload(OwnershipRequest.user))
                   .filter(OwnershipRequest.workflow_status == workflow_status)
                   .limit(per_page).offset((page -1) * per_page))
    count_stmt = (select(func.count(OwnershipRequest.request_id))
                  .where(OwnershipRequest.workflow_status == workflow_status))

    if workflow_status in ('accepted', 'rejected'):
        window = datetime.now() - timedelta(days=days_back)
        report_stmt = report_stmt.join(OwnershipRequestsAudit).filter( OwnershipRequestsAudit.date > window)
        count_stmt = count_stmt.join(OwnershipRequestsAudit).filter(OwnershipRequestsAudit.date > window)

    oreqs = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, ownership_requests=oreqs, worflow_status=workflow_status, days_back=days_back)



