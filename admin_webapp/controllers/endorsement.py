"""arXiv endorsements controllers."""
from collections import defaultdict
from datetime import datetime, timedelta
import logging
from admin_webapp.routes import endorsement

from flask import Blueprint, render_template, request, \
    make_response, current_app, Response, abort

from flask_sqlalchemy import Pagination

from sqlalchemy import select, func, case, text, insert, update, desc
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import joinedload, selectinload, aliased
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped

from arxiv_db.models import Endorsements, EndorsementsAudit, EndorsementRequests, Demographics
from arxiv_db.models.associative_tables import t_arXiv_paper_owners

from admin_webapp.extensions import get_csrf, get_db
from admin_webapp.admin_log import audit_admin
logger = logging.getLogger(__file__)

# blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')
"""
All endorsements listing
"""
def simple_endorsement_listing(per_page:int, page: int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(Endorsements)
                #    TODO: do I need a joinedload to prevent N+1 queries
                #    .options(joinedload(TapirUsers.tapir_nicknames))
                   .limit(per_page).offset((page -1) * per_page)).join(EndorsementsAudit, isouter=True)

    count_stmt = (select(func.count(Endorsements.endorsement_id)))

    endorsements = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)


    return dict(pagination=pagination, count=count, endorsements=endorsements)

def endorsement_listing(report_type:str, per_page:int, page: int, days_back:int,
                        flagged:bool, not_positive:bool=False):
    """Get data for a list of endorsement requests based on query."""
    session = get_db(current_app).session
    # depending on SQLalchemy data model sometimes arXiv_endorsements is endorsement
    report_stmt = (select(EndorsementRequests)
                   .options(joinedload(EndorsementRequests.endorsee),
                            joinedload(EndorsementRequests.arXiv_endorsements).joinedload(Endorsements.endorser),)
                   .order_by(EndorsementRequests.request_id.desc())
                   .limit(per_page).offset((page -1) * per_page))
    count_stmt = (select(func.count(EndorsementRequests.request_id)))
    if flagged:
        report_stmt = report_stmt.join(Demographics, EndorsementRequests.endorsee_id == Demographics.user_id)
        report_stmt = report_stmt.filter(Demographics.flag_suspect == 1)
        count_stmt = count_stmt.join(Demographics, EndorsementRequests.endorsee_id == Demographics.user_id)
        count_stmt = count_stmt.filter(Demographics.flag_suspect == 1)

    if not_positive:
        report_stmt = report_stmt.join(Endorsements, EndorsementRequests.request_id == Endorsements.request_id)
        report_stmt = report_stmt.filter(Endorsements.point_value <= 0)
        count_stmt = count_stmt.join(Endorsements, EndorsementRequests.request_id == Endorsements.request_id)
        count_stmt = count_stmt.filter(Endorsements.point_value <= 0)

    if report_type == 'today':
        days_back = 1
    elif not days_back:
        days_back = 7

    window = datetime.now() - timedelta(days=days_back)
    report_stmt = report_stmt.filter(EndorsementRequests.issued_when > window)
    count_stmt = count_stmt.filter(EndorsementRequests.issued_when > window)

    endorsements = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, endorsements=endorsements,
                report_type=report_type, days_back=days_back, not_positive=not_positive)
