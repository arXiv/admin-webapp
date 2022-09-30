"""arXiv paper ownership routes."""

from flask import Blueprint, render_template, url_for, request, \
    make_response, redirect, current_app, send_file, Response

from flask_sqlalchemy import get_state, Pagination

from sqlalchemy import select, func
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped

from arxiv_db.models import OwnershipRequests, OwnershipRequestsAudit

blueprint = Blueprint('ownership', __name__, url_prefix='')


@blueprint.route('/auth/v2/ownership/pending', methods=['GET'])
def pending() -> Response:
    """Pending ownership reqeusts."""
    args = request.args
    per_page = args.get('per_page', default=20, type=int)
    page = args.get('page', default=1, type=int)

    session = get_state(current_app).db.session

    stmt = (select(OwnershipRequestsAudit)
            .where(OwnershipRequests.workflow_status == 'pending')
            .limit(per_page).offset((page -1) * per_page))
    oreqs = session.scalars(stmt)

    stmt2 = (select(func.count(OwnershipRequests.request_id))
             .where(OwnershipRequests.workflow_status == 'pending'))
    count = session.execute(stmt2).scalar_one()

    pagination = Pagination(query=None, page=1, per_page=20, total=count, items=None)
    return render_template('ownership/requests.html',
                           title="Ownership Requests: Pending",
                           ownership_requests=oreqs,
                           pagination=pagination)
