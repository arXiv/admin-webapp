"""arXiv endorsement routes."""

from datetime import datetime, timedelta

from flask_sqlalchemy import Pagination

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from flask import Blueprint, render_template, Response, request, current_app

from arxiv_db.models import EndorsementRequests, Endorsements, TapirUsers, Demographics

from admin_webapp.extensions import get_db

blueprint = Blueprint('endorsement', __name__, url_prefix='/endorsement')


@blueprint.route('/request/<int:endorsement_id>', methods=['GET'])
def request_detail(endorsement_id:int) -> Response:
    """Display a endorsement."""
    data=dict(endorsement_id=endorsement_id)
    return render_template('endorsement/request_detail.html', **data)


def endorsement_listing(report_type:str, per_page:int, page: int, days_back:int,
                        flagged:bool, not_positive:bool=False):
    """Get data for a list of endorsement requests."""
    session = get_db(current_app).session
    report_stmt = (select(EndorsementRequests)
                   .options(joinedload(EndorsementRequests.endorsee),
                            joinedload(EndorsementRequests.endorsement).joinedload(Endorsements.endorser),)
                   .order_by(EndorsementRequests.request_id.desc())
                   .limit(per_page).offset((page -1) * per_page))
    count_stmt = (select(func.count(EndorsementRequests.request_id)))
    if flagged:
        report_stmt = report_stmt.join(Demographics, EndorsementRequests.endorsee_id == Demographics.user_id)
        report_stmt = report_stmt.filter(Demographics.flag_suspect == 1)
        count_stmt = count_stmt.join(Demographics, EndorsementRequests.endorsee_id == Demographics.user_id)
        count_stmt = count_stmt.filter(Demographics.flag_suspect == 1)

    if not_positive:
        report_stmt = report_stmt.filter(EndorsementRequests.point_value <= 0)
        count_stmt = count_stmt.filter(EndorsementRequests.point_value <= 0)

    if not days_back:
        if report_type == 'today':
            days_back = 1
        if report_type == 'last_week':
            days_back = 7

    window = datetime.now() - timedelta(days=days_back)
    report_stmt = report_stmt.filter(EndorsementRequests.issued_when > window)
    count_stmt = count_stmt.filter(EndorsementRequests.issued_when > window)

    endorsements = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, endorsements=endorsements,
                report_type=report_type, days_back=days_back, not_positive=not_positive)


@blueprint.route('/requests/today', methods=['GET'])
def today() -> Response:
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    flagged = args.get('flagged', default=0, type=int)
    days_back = args.get('days_back', default=7, type=int)
    data = endorsement_listing('today', per_page, page, days_back, flagged)
    data['title'] = "Today's Endorsement Requests"
    return render_template('endorsement/list.html', **data)


@blueprint.route('/requests/last_week', methods=['GET'])
def last_week() -> Response:
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    flagged = args.get('flagged', default=0, type=int)
    days_back = args.get('days_back', default=7, type=int)
    data = endorsement_listing('last_week', per_page, page, days_back, flagged)
    data['title'] = f"Endorsement Requests Last {days_back} Days"
    return render_template('endorsement/list.html', **data)


@blueprint.route('/requests/negative', methods=['GET'])
def negative() -> Response:
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    days_back = args.get('days_back', default=7, type=int)
    data = endorsement_listing('negative', per_page, page, days_back, False, not_positive=1)
    data['title'] = "Negative Endorsement Requests"
    return render_template('endorsement/list.html', **data)
