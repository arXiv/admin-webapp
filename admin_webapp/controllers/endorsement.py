"""arXiv Endorsement controllers."""
from collections import defaultdict
from datetime import datetime, timedelta
import logging

from flask import Blueprint, render_template, request, \
    make_response, current_app, Response, abort

from sqlalchemy import select, func, case, text, insert, update, desc
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import joinedload, selectinload, aliased
from arxiv.base import logging

from arxiv.auth.auth.decorators import scoped
from arxiv.db import session
from arxiv.db.models import Endorsement, EndorsementsAudit, EndorsementRequest, Demographic

from .util import Pagination
logger = logging.getLogger(__file__)

# blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')
"""
All Endorsement listing
"""
def simple_endorsement_listing(per_page:int, page: int) -> dict:
    report_stmt = (select(Endorsement)
                #    TODO: do I need a joinedload to prevent N+1 queries
                #    .options(joinedload(TapirUsers.tapir_nicknames))
                   .limit(per_page).offset((page -1) * per_page)).join(EndorsementsAudit, isouter=True)

    count_stmt = (select(func.count(Endorsement.endorsement_id)))

    Endorsement = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)


    return dict(pagination=pagination, count=count, Endorsement=Endorsement)

def endorsement_listing(report_type:str, per_page:int, page: int, days_back:int,
                        flagged:bool, not_positive:bool=False):
    """Get data for a list of endorsement requests based on query."""
    # depending on SQLalchemy data model sometimes arXiv_Endorsement is endorsement
    report_stmt = (select(EndorsementRequest)
                   .options(joinedload(EndorsementRequest.endorsee),
                            joinedload(EndorsementRequest.arXiv_Endorsement).joinedload(Endorsement.endorser),)
                   .order_by(EndorsementRequest.request_id.desc())
                   .limit(per_page).offset((page -1) * per_page))
    count_stmt = (select(func.count(EndorsementRequest.request_id)))
    if flagged:
        report_stmt = report_stmt.join(Demographic, EndorsementRequest.endorsee_id == Demographic.user_id)
        report_stmt = report_stmt.filter(Demographic.flag_suspect == 1)
        count_stmt = count_stmt.join(Demographic, EndorsementRequest.endorsee_id == Demographic.user_id)
        count_stmt = count_stmt.filter(Demographic.flag_suspect == 1)

    if not_positive:
        report_stmt = report_stmt.join(Endorsement, EndorsementRequest.request_id == Endorsement.request_id)
        report_stmt = report_stmt.filter(Endorsement.point_value <= 0)
        count_stmt = count_stmt.join(Endorsement, EndorsementRequest.request_id == Endorsement.request_id)
        count_stmt = count_stmt.filter(Endorsement.point_value <= 0)

    if report_type == 'today':
        days_back = 1
    elif not days_back:
        days_back = 7

    window = datetime.now() - timedelta(days=days_back)
    report_stmt = report_stmt.filter(EndorsementRequest.issued_when > window)
    count_stmt = count_stmt.filter(EndorsementRequest.issued_when > window)

    Endorsement = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, Endorsement=Endorsement,
                report_type=report_type, days_back=days_back, not_positive=not_positive)

"""
Get count information for landing page.
"""
def endorsement_listing_counts_only(report_type:str, flagged:bool=False, not_positive:bool=False):
    count_stmt = (select(func.count(EndorsementRequest.request_id)))
    if flagged:
        count_stmt = count_stmt.join(Demographic, EndorsementRequest.endorsee_id == Demographic.user_id)
        count_stmt = count_stmt.filter(Demographic.flag_suspect == 1)

    if not_positive:
        count_stmt = count_stmt.join(Endorsement, EndorsementRequest.request_id == Endorsement.request_id)
        count_stmt = count_stmt.filter(Endorsement.point_value <= 0)
  
    if report_type == 'today':
        days_back = 1
    else:
        days_back = 7
    window = datetime.now() - timedelta(days=days_back)
    count_stmt = count_stmt.filter(EndorsementRequest.issued_when > window)
    count = session.execute(count_stmt).scalar_one()

    return count