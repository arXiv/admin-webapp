"""arXiv paper ownership routes."""

from flask import Blueprint, render_template, url_for, request, \
    make_response, redirect, current_app, send_file, Response

from flask_sqlalchemy import get_state

from sqlalchemy import select
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped

from arxiv_db.models import OwnershipRequests, OwnershipRequestsAudit

blueprint = Blueprint('ownership', __name__, url_prefix='')


@blueprint.route('/auth/v2/ownership/requests')
def ownerhsip_requests() -> Response:
    """Ownership reqeusts."""

    db = get_state(current_app).db
    stmt = select(OwnershipRequestsAudit).limit(10)
    oreqs = db.session.scalars(stmt)
    breakpoint();
    return render_template('ownership/requests.html', ownership_requests=oreqs)
