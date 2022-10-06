"""arXiv paper ownership routes."""

from datetime import datetime, timedelta
import logging

from flask import Blueprint, render_template, request, \
    make_response, current_app, Response, abort

from flask_sqlalchemy import Pagination

from sqlalchemy import select, func, text, insert, update
from sqlalchemy.orm import joinedload, selectinload
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped
from admin_webapp.extensions import get_csrf, get_db
from arxiv_db.models import OwnershipRequests, OwnershipRequestsAudit, TapirUsers, Documents
from arxiv_db.models.associative_tables import t_arXiv_paper_owners

from admin_webapp.controllers.ownership import ownership_detail, ownership_listing, ownership_post

logger = logging.getLogger(__file__)

blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')


@blueprint.route('/<int:ownership_id>', methods=['GET', 'POST'])
def display(ownership_id:int) -> Response:
    if request.method == 'GET':
        return render_template('ownership/display.html',**ownership_detail(ownership_id, None))
    elif request.method == 'POST':
        return render_template('ownership/display.html', **ownership_detail(ownership_id, ownership_post))


# @blueprint.route('/<int:ownership_id>', methods=['GET', 'POST'])
# def display(ownership_id:int) -> Response:
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


    On POST:

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

    data={}
    already_ownes =[paper.paper_id for paper in oreq.user.owned_papers]
    # TODO all of these need a success method
    if request.method == 'POST':
        get_csrf(current_app).protect()
        admin_id = 1234 #request.auth.user.user_id

        breakpoint()
        if 'make_owner' in request.form:
            docs_to_own = [ key.split('_')[1] for key, value in request.form.items()
                            if key.startswith('approve_')]
            is_author = 1 if request.form['is_author'] else 0

            #todo add this to config:
            cookie = request.cookies.get(current_app.config['CLASSIC_TRACKING_COOKIE'])
            now = int(datetime.now().astimezone(current_app.config['ARXIV_BUSINESS_TZ']).timestamp())
            for doc_id in docs_to_own:
                stmt = insert(t_arXiv_paper_owners).values(
                    document_id=doc_id, user_id=oreq.user.user_id, date=now,
                    added_by=admin_id, remote_addr=request.remote_addr, tracking_cookie=cookie,
                    flag_auto=0, flag_author=is_author)
                session.execute(stmt)

            # TODO add admin log (user_id 'add-paper-owner-2' doc_id)
            # user_id is the affected_user,
            oreq.workflow_status = 'accepted'
            session.execute(update(OwnershipRequests)
                            .where(OwnershipRequests.request_id == ownership_id)
                            .values(workflow_status = 'accepted'))
            data['success']='accepted'
        elif 'reject' in request.form:
            stmt=text("""UPDATE arXiv_ownership_requests SET workflow_status='rejected'
            WHERE request_id=:reqid""")
            session.execute(stmt, dict(reqid=oreq.request_id))
            data['success']='rejected'
        elif 'revisit' in request.form:
            stmt=text("""UPDATE arXiv_ownership_requests SET workflow_status='pending'
            WHERE request_id=:reqid""")
            session.execute(stmt, dict(reqid=oreq.request_id))
            data['success']='revisited'
        else:
            abort(400)

        session.commit()

    docids= [paper.paper_id for paper in oreq.documents]
    stmt=(select(Documents)
          .filter(Documents.submitter_email.in_(set([paper.submitter_email for paper in oreq.documents])))
          .filter(Documents.paper_id.not_in(docids)))
    other_papers = session.scalars(stmt)

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
                                  docids = docids),
                           **data)


@blueprint.route('/pending', methods=['GET'])
def pending() -> Response:
    """Pending ownership reqeusts."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)

    data = ownership_listing('pending', per_page, page, 0)
    data['title'] = "Ownership Reqeusts: Pending"
    return render_template('ownership/list.html',
                           **data)


@blueprint.route('/accepted', methods=['GET'])
def accepted() -> Response:
    """Accepted ownership reqeusts."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    days_back = args.get('days_back', default=7, type=int)

    data = ownership_listing('accepted', per_page, page, days_back=days_back)
    data['title'] = f"Ownership Reqeusts: accepted last {days_back} days"
    return render_template('ownership/list.html',
                           **data)


@blueprint.route('/rejected', methods=['GET'])
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
