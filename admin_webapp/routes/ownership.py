"""arXiv paper ownership routes."""

from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, \
    make_response, current_app, Response, abort

from flask_sqlalchemy import Pagination

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped
from admin_webapp.db import get_db

from arxiv_db.models import OwnershipRequests, OwnershipRequestsAudit, TapirUsers, Documents

blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')


@blueprint.route('/<int:ownership_id>', methods=['GET'])
def display(ownership_id:int) -> Response:
    """Display a ownership request.

    Need to display:

    * User Information
    * Link to E-mail history
    * Information about request
    * Papers

    We'd like to (1) extract E-mail address for papers,
    and see if there are more with the same address

    Present options:

    * Grant authorship of any/all papers
    * Grant authorhsip to papers that have same submission E-mail
    """
    session = get_db(current_app).session
    stmt = (select(OwnershipRequests)
            .options(
                joinedload(OwnershipRequests.user).joinedload(TapirUsers.tapir_nicknames),
                joinedload(OwnershipRequests.user).joinedload(TapirUsers.owned_papers),
                joinedload(OwnershipRequests.request_audit),
                joinedload(OwnershipRequests.documents),
            )
            .where( OwnershipRequests.request_id == ownership_id))
    oreq = session.scalar(stmt)
    if not oreq:
        abort(404)

    already_ownes =[paper.paper_id for paper in oreq.user.owned_papers]
    docids= [paper.paper_id for paper in oreq.documents] + already_ownes
    other_papers=[]
    for email in  set([paper.submitter_email for paper in oreq.documents]):
        stmt=(select(Documents)
              .where(Documents.submitter_email == email)
              .where(Documents.document_id.not_in(docids)))
        more=session.scalars(stmt)
        other_papers.extend(more)

    for paper in oreq.documents:
        setattr(paper, 'already_ownes', paper.paper_id in already_ownes)

    # TODO Handle POST of reject, make_owner_author, make_owner_not_author
    # TODO approved when user is in author list
    # TODO things related to endorsement
    return render_template('ownership/display.html',
                           **dict(ownership=oreq,
                                  user=oreq.user,
                                  nickname= oreq.user.tapir_nicknames[0].nickname,
                                  papers=oreq.documents,
                                  audit=oreq.request_audit[0],
                                  ownership_id=ownership_id,
                                  other_papers=other_papers,
                                  docids = docids))

@blueprint.route('/pending', methods=['GET'])
def pending() -> Response:
    """Pending ownership reqeusts."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)

    data = _ownership_listing('pending', per_page, page, 0)
    data['title'] = "Ownership Reqeusts: Pending"
    return render_template('ownership/requests.html',
                           **data)


@blueprint.route('/accepted', methods=['GET'])
def accepted() -> Response:
    """Accepted ownership reqeusts."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    days_back = args.get('days_back', default=7, type=int)

    data = _ownership_listing('accepted', per_page, page, days_back=days_back)
    data['title'] = f"Ownership Reqeusts: accepted last {days_back} days"
    return render_template('ownership/requests.html',
                           **data)


@blueprint.route('/rejected', methods=['GET'])
def rejected() -> Response:
    """Rejected ownership reqeusts."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    days_back = args.get('days_back', default=7, type=int)

    data = _ownership_listing('rejected', per_page, page, days_back=days_back)
    data['title'] = f"Ownership Reqeusts: Rejected last {days_back} days"
    return render_template('ownership/requests.html',
                           **data)



def _ownership_listing(workflow_status:str, per_page:int, page: int,
                       days_back:int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(OwnershipRequestsAudit)
                   .options(selectinload(OwnershipRequestsAudit.user))
                   .filter(OwnershipRequests.workflow_status == workflow_status)
                   .limit(per_page).offset((page -1) * per_page))
    count_stmt = (select(func.count(OwnershipRequests.request_id))
                  .where(OwnershipRequests.workflow_status == workflow_status))

    if workflow_status in ('accepted', 'rejected'):
        now = datetime.now() - timedelta(days=days_back)
        report_stmt = report_stmt.filter(OwnershipRequestsAudit.date > now.timestamp())
        count_stmt = count_stmt.filter(OwnershipRequestsAudit.date > now.timestamp())

    oreqs = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, ownership_requests=oreqs, worflow_status=workflow_status, days_back=days_back)
