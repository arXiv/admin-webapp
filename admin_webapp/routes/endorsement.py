"""arXiv endorsement routes."""

from datetime import datetime, timedelta

from flask_sqlalchemy import Pagination

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from admin_webapp.controllers.endorsement import endorsement_listing

from flask import Blueprint, render_template, Response, request, current_app, abort, redirect, url_for, make_response

from wtforms import SelectField, BooleanField, StringField, validators
from flask_wtf import FlaskForm

from arxiv_db.models import EndorsementRequests, Endorsements, TapirUsers, Demographics

from arxiv.base.alerts import flash_failure

from admin_webapp.extensions import get_db


blueprint = Blueprint('endorsement', __name__, url_prefix='/endorsement')


@blueprint.route('/request/<int:endorsement_req_id>', methods=['GET'])
def request_detail(endorsement_req_id:int) -> Response:
    """Display a single request for endorsement."""
    session = get_db(current_app).session
    stmt = (select(EndorsementRequests)
            .options(joinedload(EndorsementRequests.endorsee).joinedload(TapirUsers.tapir_nicknames),
                     joinedload(EndorsementRequests.endorsement).joinedload(Endorsements.endorser).joinedload(TapirUsers.tapir_nicknames),
                     joinedload(EndorsementRequests.audit))
            .filter(EndorsementRequests.request_id == endorsement_req_id)
            )
    endo_req = session.execute(stmt).scalar() or abort(404)
    return render_template('endorsement/request_detail.html',
                           **dict(endorsement_req_id=endorsement_req_id,
                                  endo_req=endo_req,
                                  ))

@blueprint.route('/request/<int:endorsement_req_id>/flip_valid', methods=['POST'])
def flip_valid(endorsement_req_id:int) -> Response:
    """Flip an endorsement_req valid column."""
    session = get_db(current_app).session
    stmt = (select(EndorsementRequests)
            .options(joinedload(EndorsementRequests.endorsement))
            .filter(EndorsementRequests.request_id == endorsement_req_id))
    endo_req = session.execute(stmt).scalar() or abort(404)
    endo_req.endorsement.flag_valid = not bool(endo_req.endorsement.flag_valid)
    session.commit()
    return redirect(url_for('endorsement.request_detail', endorsement_req_id=endorsement_req_id))


@blueprint.route('/request/<int:endorsement_req_id>/flip_score', methods=['POST'])
def flip_score(endorsement_req_id:int) -> Response:
    """Flip an endorsement_req score."""
    session = get_db(current_app).session
    stmt = (select(EndorsementRequests)
            .options(joinedload(EndorsementRequests.endorsement))
            .filter(EndorsementRequests.request_id == endorsement_req_id))
    endo_req = session.execute(stmt).scalar() or abort(404)
    if endo_req.endorsement.point_value > 0:
        endo_req.endorsement.point_value = 0
    else:
        endo_req.endorsement.point_value = 10

    session.commit()
    return redirect(url_for('endorsement.request_detail', endorsement_req_id=endorsement_req_id))


@blueprint.route('/<int:endorsement_id>', methods=['GET'])
def detail(endorsement_id: int) -> Response:
    """Display a single endorsement."""
    abort(500)

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


@blueprint.route('/requests/today', methods=['GET'])
def today() -> Response:
    """Reports todays endorsement requests."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    flagged = args.get('flagged', default=0, type=int)
    _check_report_args(per_page, page, 0, flagged)
    data = endorsement_listing('today', per_page, page, 0, flagged)
    data['title'] = f"Today's {'Flagged ' if flagged else ''}Endorsement Requests"
    return render_template('endorsement/list.html', **data)


@blueprint.route('/requests/last_week', methods=['GET'])
def last_week() -> Response:
    """Reports last 7 days endorsement requests."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    flagged = args.get('flagged', default=0, type=int)
    days_back = args.get('days_back', default=7, type=int)
    _check_report_args(per_page, page, days_back, flagged)
    data = endorsement_listing('last_week', per_page, page, days_back, flagged)
    data['title'] = f"Endorsement {'Flagged ' if flagged else ''}Requests Last {days_back} Days"
    return render_template('endorsement/list.html', **data)


@blueprint.route('/requests/negative', methods=['GET'])
def negative() -> Response:
    """Reports non-positive scored  endorsement requests for last 7 days."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    days_back = args.get('days_back', default=7, type=int)
    _check_report_args(per_page, page, days_back, 0)
    data = endorsement_listing('negative', per_page, page, days_back, False, not_positive=True)
    data['title'] = "Negative Endorsement Requests"
    return render_template('endorsement/list.html', **data)


def _check_report_args(per_page, page, days_back, flagged):
    if per_page > 1000:
        abort(400)
    if page > 10000:
        abort(400)
    if days_back > 365 * 10:
        abort(400)
    if flagged not in [1, 0]:
        abort(400)


@blueprint.route('/endorse', methods=['GET', 'POST'])
def endorse() -> Response:
    """Endorse page."""

    # TODO check veto_status == no-endorse and mesage similar to no-endorse-screen.php

    if request.method == 'GET':
        return render_template('endorsement/endorse.html')
    # elif request.method == 'POST' and not request.form.get('x',None):
    #     flash_failure("You must enger a non-blank endorsement code.")
    #     return make_response(render_template('endorsement/endorse.html'), 400)

    form = EndorseStage2Form()

    session = get_db(current_app).session
    endo_code = request.form.get('x')
    stmt = (select(EndorsementRequests)
            .limit(1)
            #.filter(EndorsementRequests.secret == endo_code)
            )
    endoreq = session.scalar(stmt)

    if not endoreq:
        flash_failure("The endorsement codes is not valid. It has never been issued.")
        return make_response(render_template('endorsement/endorse.html'), 400)

    if not endoreq.flag_valid:
        flash_failure("The endorsement code is not valid. It has either expired or been deactivated.")
        return make_response(render_template('endorsement/endorse.html'), 400)

    category = f"{endoreq.archive}.{endoreq.subject_class}" if endoreq.subject_class else endoreq.archive
    category_display = get_category_display(category)

    if endoreq.endorsee_id == reqeust.auth.user.user_id:
        return make_response(render_template('endorsement/no-self-endorse.html'), 400)


    if request.method == 'POST' and reqeust.form.get('choice', None):
        form.validate()
        # TODO Do save?


    data=dict(endorsee=endoreq.endorsee,
              endorsement=endoreq.endorsement,
              form = form,
              )

    return render_template('endorsement/endorse-stage2.html', **data)

class EndorseStage2Form(FlaskForm):
    """Form for stage 2 of endorse."""
    choice = SelectField('choice',
                         [validators.InputRequired(), validators.AnyOf(['do','do not'])],
                         choices=[(None,'-- choose --'),('do','do'),('do not','do not')])
    knows_personally = BooleanField('knows_personally')
    seen_paper = BooleanField('seen_paper')
    comment = StringField('comment')
