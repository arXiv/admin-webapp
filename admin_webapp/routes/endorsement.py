"""arXiv endorsement routes."""

from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from flask import Blueprint, render_template, Response, request, current_app, abort, redirect, url_for, make_response

from wtforms import SelectField, BooleanField, StringField, validators
from flask_wtf import FlaskForm

from . import admin_scoped
# need to refactor this back into a controller
from arxiv.db.models import EndorsementRequest, Endorsement, TapirUser
from arxiv.db import session
from arxiv.base.alerts import flash_failure

from admin_webapp.controllers.endorsement import endorsement_listing # multiple implementations of listing here

blueprint = Blueprint('endorsement', __name__, url_prefix='/endorsement')

@blueprint.route('/all', methods=['GET'])
@admin_scoped
def endorsements() -> Response:
    """
    Show administrators view
    """
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    
    data = endorsement_listing(per_page, page)
    data['title'] = "Endorsement"
    return render_template('endorsement/list.html', **data)

@blueprint.route('/request/<int:endorsement_req_id>', methods=['GET'])
@admin_scoped
def request_detail(endorsement_req_id:int) -> Response:
    """Display a single request for endorsement."""
    stmt = (select(EndorsementRequest)
            .options(joinedload(EndorsementRequest.endorsee).joinedload(TapirUser.tapir_nicknames),
                     joinedload(EndorsementRequest.endorsement).joinedload(Endorsement.endorser).joinedload(TapirUser.tapir_nicknames),
                     joinedload(EndorsementRequest.audit))
            .filter(EndorsementRequest.request_id == endorsement_req_id)
            )
    endo_req = session.execute(stmt).scalar() or abort(404)
    return render_template('endorsement/request_detail.html',
                           **dict(endorsement_req_id=endorsement_req_id,
                                  endo_req=endo_req,
                                  ))
    return render_template('endorsement/display.html')

@blueprint.route('/request/<int:endorsement_req_id>/flip_valid', methods=['POST'])
@admin_scoped
def flip_valid(endorsement_req_id:int) -> Response:
    """Flip an endorsement_req valid column."""
    stmt = (select(EndorsementRequest)
            .options(joinedload(EndorsementRequest.endorsement))
            .filter(EndorsementRequest.request_id == endorsement_req_id))
    endo_req = session.execute(stmt).scalar() or abort(404)
    endo_req.endorsement.flag_valid = not bool(endo_req.endorsement.flag_valid)
    session.commit()
    return redirect(url_for('endorsement.request_detail', endorsement_req_id=endorsement_req_id))

@blueprint.route('/request/<int:endorsement_req_id>/flip_score', methods=['POST'])
@admin_scoped
def flip_score(endorsement_req_id:int) -> Response:
    """Flip an endorsement_req score."""
    stmt = (select(EndorsementRequest)
            .options(joinedload(EndorsementRequest.endorsement))
            .filter(EndorsementRequest.request_id == endorsement_req_id))
    endo_req = session.execute(stmt).scalar() or abort(404)
    if endo_req.endorsement.point_value > 0:
        endo_req.endorsement.point_value = 0
    else:
        endo_req.endorsement.point_value = 10

    session.commit()
    return redirect(url_for('endorsement.request_detail', endorsement_req_id=endorsement_req_id))

@blueprint.route('/<int:endorsement_id>', methods=['GET'])
@admin_scoped
def detail(endorsement_id: int) -> Response:
    """Display a single endorsement."""
    abort(500)

@blueprint.route('/requests/today', methods=['GET'])
@admin_scoped
def today() -> Response:
    """Reports today's endorsement requests."""
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    flagged = args.get('flagged', default=0, type=int)
    _check_report_args(per_page, page, 0, flagged)
    data = endorsement_listing('today', per_page, page, 0, flagged)
    data['title'] = f"Today's {'Flagged ' if flagged else ''}Endorsement Requests"
    return render_template('endorsement/list.html', **data)

def _check_report_args(per_page, page, days_back, flagged):
    if per_page > 1000:
        abort(400)
    if page > 10000:
        abort(400)
    # will not show data older than 10 years
    if days_back > 365 * 10:
        abort(400)
    if flagged not in [1, 0]:
        abort(400)

@blueprint.route('/requests/last_week', methods=['GET'])
@admin_scoped
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
@admin_scoped
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

"""
New feature for approved and blocked user list
"""
@blueprint.route('/modify', methods=['GET'])
@admin_scoped
def modify_form() -> Response:
    """Modify lists"""
    return render_template('endorsement/modify.html')

@blueprint.route('/endorse', methods=['GET', 'POST'])
@admin_scoped
def endorse() -> Response:
    """Endorse page."""

    # TODO check veto_status == no-endorse and mesage similar to no-endorse-screen.php

    if request.method == 'GET':
        return render_template('endorsement/endorse.html')
    # elif request.method == 'POST' and not request.form.get('x',None):
    #     flash_failure("You must enger a non-blank endorsement code.")
    #     return make_response(render_template('endorsement/endorse.html'), 400)

    form = EndorseStage2Form()

    endo_code = request.form.get('x')
    stmt = (select(EndorsementRequest)
            .limit(1)
            #.filter(EndorsementRequest.secret == endo_code)
            )
    endoreq = session.scalar(stmt)

    if not endoreq:
        flash_failure("The endorsement codes is not valid. It has never been issued.")
        return make_response(render_template('endorsement/endorse.html'), 400)

    if not endoreq.flag_valid:
        flash_failure("The endorsement code is not valid. It has either expired or been deactivated.")
        return make_response(render_template('endorsement/endorse.html'), 400)

    category = f"{endoreq.archive}.{endoreq.subject_class}" if endoreq.subject_class else endoreq.archive

    if endoreq.endorsee_id == request.auth.user.user_id:
        return make_response(render_template('endorsement/no-self-endorse.html'), 400)


    if request.method == 'POST' and request.form.get('choice', None):
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