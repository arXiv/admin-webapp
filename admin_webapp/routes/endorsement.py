"""arXiv endorsement routes."""

from flask import Blueprint, render_template, url_for, request, \
    make_response, redirect, current_app, send_file, Response, flash

from flask_sqlalchemy import get_state, Pagination

from sqlalchemy import select, func

from arxiv_auth.auth.decorators import scoped


blueprint = Blueprint('endorsement', __name__, url_prefix='/endorsement')


@blueprint.route('/request', methods=['GET'])
def display() -> Response:
    return render_template('endorsement/display.html')
