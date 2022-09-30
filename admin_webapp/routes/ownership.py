"""arXiv paper ownership routes."""

from datetime import datetime, timedelta

from flask import Blueprint, render_template, url_for, request, \
    make_response, redirect, current_app, send_file, Response, flash

from flask_sqlalchemy import get_state, Pagination

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped

from arxiv_db.models import OwnershipRequests, OwnershipRequestsAudit, TapirUsers

blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')


@blueprint.route('/display', methods=['GET'])
def display() -> Response:
    return render_template('ownership/display.html')

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
    """accepted ownership reqeusts."""
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
    session = get_state(current_app).db.session

    stmt = (select(OwnershipRequestsAudit)
            .options(selectinload(OwnershipRequestsAudit.user))
            .filter(OwnershipRequests.workflow_status == workflow_status))

    if workflow_status in ('accepted', 'rejected'):
        now = datetime.now() - timedelta(days=days_back)
        stmt = stmt.filter(OwnershipRequestsAudit.date > now.timestamp())

    stmt = stmt.limit(per_page).offset((page -1) * per_page)
    oreqs = session.scalars(stmt)

    stmt2 = (select(func.count(OwnershipRequests.request_id))
             .where(OwnershipRequests.workflow_status == 'pending'))
    count = session.execute(stmt2).scalar_one()

    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, ownership_requests=oreqs, worflow_status=workflow_status, days_back=days_back)
