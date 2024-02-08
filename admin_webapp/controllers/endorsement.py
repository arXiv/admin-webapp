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

from arxiv_db.models import Endorsements, EndorsementsAudit
#from arxiv_db.models.associative_tables import t_arXiv_paper_owners

from admin_webapp.extensions import get_csrf, get_db
from admin_webapp.admin_log import audit_admin
logger = logging.getLogger(__file__)

# blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')
"""
All endorsements listing
"""
def endorsement_listing(per_page:int, page: int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(Endorsements)
                #    TODO: do I need a joinedload to prevent N+1 queries
                #    .options(joinedload(TapirUsers.tapir_nicknames))
                   .join(EndorsementsAudit, Endorsements.endorsement_id, isouter=True)
                   .limit(per_page).offset((page -1) * per_page))

    count_stmt = (select(func.count(Endorsements.endorsement_id)))

    endorsements = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)

    # for e in endorsements:
    #     print(e)
    return dict(pagination=pagination, count=count, endorsements=endorsements)

