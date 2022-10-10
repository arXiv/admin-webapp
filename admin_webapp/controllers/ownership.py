"""arXiv paper ownership controllers."""

from datetime import datetime, timedelta
import logging

from flask import Blueprint, request, \
    current_app, Response, abort

from flask_sqlalchemy import Pagination

from sqlalchemy import select, func, text, insert, update
from sqlalchemy.orm import joinedload
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped

from arxiv_db.models import OwnershipRequests, OwnershipRequestsAudit, TapirUsers, Documents, EndorsementRequests
from arxiv_db.models.associative_tables import t_arXiv_paper_owners

from admin_webapp.extensions import get_db
from admin_webapp.admin_log import audit_admin

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
    session = get_db(current_app).session
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
            now = int(datetime.now().astimezone(current_app.config['ARXIV_BUSINESS_TZ']).timestamp())

            for doc_id in to_add_ownership:
                stmt = insert(t_arXiv_paper_owners).values(
                    document_id=doc_id, user_id=oreq.user.user_id, date=now,
                    added_by=admin_id, remote_addr=request.remote_addr, tracking_cookie=cookie,
                    flag_auto=0, flag_author=is_author)
                session.execute(stmt)
                #audit_admin(oreq.user_id, 'add-paper-owner-2', doc_id)

            oreq.workflow_status = 'accepted'
            session.execute(update(OwnershipRequests)
                            .where(OwnershipRequests.request_id == oreq.request_id)
                            .values(workflow_status = 'accepted'))

            data['success']='accepted'
            data['success_count'] = len(docs_to_own - already_owns)
            data['success_already_owned'] = len(docs_to_own & already_owns)
        elif 'reject' in request.form:
            stmt=text("""UPDATE arXiv_ownership_requests SET workflow_status='rejected'
            WHERE request_id=:reqid""")
            session.execute(stmt, dict(reqid=oreq.request_id))
            data['success']='rejected'
        elif 'revisit' in request.form:
            # A revisit does not undo the paper ownership. This the same as legacy.
            stmt=text("""UPDATE arXiv_ownership_requests SET workflow_status='pending'
            WHERE request_id=:reqid""")
            session.execute(stmt, dict(reqid=oreq.request_id))
            data['success']='revisited'
        else:
            abort(400)

    session.commit()
    return data


@blueprint.route('/<int:ownership_id>', methods=['GET', 'POST'])
def ownership_detail(ownership_id:int, postfn=None) -> dict:
    """Display a ownership request.

    """
    session = get_db(current_app).session
    stmt = (select(OwnershipRequests)
            .options(
                joinedload(OwnershipRequests.user).joinedload(TapirUsers.tapir_nicknames),
                joinedload(OwnershipRequests.user).joinedload(TapirUsers.owned_papers),
                joinedload(OwnershipRequests.request_audit),
                joinedload(OwnershipRequests.documents),
                joinedload(OwnershipRequests.endorsement_request).joinedload(EndorsementRequests.audit)
            )
            .where( OwnershipRequests.request_id == ownership_id))
    oreq = session.scalar(stmt)
    if not oreq:
        abort(404)

    already_owns =[paper.paper_id for paper in oreq.user.owned_papers]
    for paper in oreq.documents:
        setattr(paper, 'already_owns', paper.paper_id in already_owns)

    endorsement_req = oreq.endorsement_request if oreq.endorsement_request else None
    data = dict(ownership=oreq,
                user=oreq.user,
                nickname= oreq.user.tapir_nicknames[0].nickname,
                papers=oreq.documents,
                audit=oreq.request_audit[0],
                ownership_id=ownership_id,
                docids =  [paper.paper_id for paper in oreq.documents],
                endorsement_req=endorsement_req,)

    if postfn:
        data=postfn(data)

    return data

def ownership_listing(workflow_status:str, per_page:int, page: int,
                       days_back:int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(OwnershipRequests)
                   .options(joinedload(OwnershipRequests.user))
                   .filter(OwnershipRequests.workflow_status == workflow_status)
                   .limit(per_page).offset((page -1) * per_page))
    count_stmt = (select(func.count(OwnershipRequests.request_id))
                  .where(OwnershipRequests.workflow_status == workflow_status))

    if workflow_status in ('accepted', 'rejected'):
        window = datetime.now() - timedelta(days=days_back)
        report_stmt = report_stmt.join(OwnershipRequestsAudit).filter( OwnershipRequestsAudit.date > window)
        count_stmt = count_stmt.join(OwnershipRequestsAudit).filter(OwnershipRequestsAudit.date > window)

    oreqs = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, ownership_requests=oreqs, worflow_status=workflow_status, days_back=days_back)
