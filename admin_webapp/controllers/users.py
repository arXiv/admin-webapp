"""arXiv paper users controllers."""

from datetime import datetime, timedelta
import logging
from admin_webapp.routes import endorsement

from flask import Blueprint, render_template, request, \
    make_response, current_app, Response, abort

from flask_sqlalchemy import Pagination

from sqlalchemy import select, func, text, insert, update
from sqlalchemy.orm import joinedload, selectinload
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped

from arxiv_db.models import TapirUsers, Documents, EndorsementRequests, Demographics
from arxiv_db.models.associative_tables import t_arXiv_paper_owners

from admin_webapp.extensions import get_csrf, get_db
from admin_webapp.admin_log import audit_admin

logger = logging.getLogger(__file__)

# blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')
"""
Get user profile
"""
def user_profile(user_id:int) -> Response:
    session = get_db(current_app).session
    stmt = (select(TapirUsers)
            .where(
                TapirUsers.user_id == user_id
            ))
    user = session.scalar(stmt)
    # TODO: optimize this so we can join with the Tapir Users rather than separate query?
    demographics_stmt = (select(Demographics)
                         .where(
                             Demographics.user_id == user_id
                         ))
    demographics = session.scalar(demographics_stmt)

    if not user or not demographics:
        abort(404)
    
    data = dict(user=user, demographics=demographics)
    return data


def administrator_listing(per_page:int, page: int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(TapirUsers)
                #    TODO: do I need a joinedload to prevent N+1 queries
                #    .options(joinedload(TapirUsers.tapir_nicknames))
                   .filter(TapirUsers.policy_class == 1) # admin policy class
                   .limit(per_page).offset((page -1) * per_page))

    count_stmt = (select(func.count(TapirUsers.user_id))
                  .where(TapirUsers.policy_class == 1))

    # if workflow_status in ('accepted', 'rejected'):
    #     window = datetime.now() - timedelta(days=days_back)
    #     report_stmt = report_stmt.join(OwnershipRequestsAudit).filter( OwnershipRequestsAudit.date > window)
    #     count_stmt = count_stmt.join(OwnershipRequestsAudit).filter(OwnershipRequestsAudit.date > window)

    users = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, users=users)

def administrator_edit_sys_listing(per_page:int, page: int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(TapirUsers)
                #    TODO: do I need a joinedload to prevent N+1 queries
                #    .options(joinedload(TapirUsers.tapir_nicknames))
                   .filter(TapirUsers.policy_class == 1) # admin policy class
                   .filter(TapirUsers.flag_edit_system == 1)
                   .limit(per_page).offset((page -1) * per_page))

    count_stmt = (select(func.count(TapirUsers.user_id))
                  .where(TapirUsers.flag_edit_system == 1)
                  .where(TapirUsers.policy_class == 1))

    users = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, users=users)


# TODO: this is broken because of a faulty TapirUser-Demographic relationship
def suspect_listing(per_page:int, page: int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(TapirUsers)
                   .options(joinedload(TapirUsers.demographics))
                   .filter(Demographics.flag_suspect == "1")
                   .limit(per_page).offset((page -1) * per_page))

    count_stmt = (select(func.count(TapirUsers.user_id))
                  .where(Demographics.flag_suspect == "1"))

    users = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, users=users)
