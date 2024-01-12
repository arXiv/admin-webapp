"""arXiv endorsement routes."""

from flask import Blueprint, render_template, Response

blueprint = Blueprint('endorsement', __name__, url_prefix='/endorsement')


@blueprint.route('/request', methods=['GET'])
def request_detail() -> Response:
    """Display a endorsement."""
    return render_template('endorsement/display.html')

@blueprint.route('/modify', methods=['GET'])
def modify_form() -> Response:
    """Modify lists"""
    return render_template('endorsement/modify.html')
