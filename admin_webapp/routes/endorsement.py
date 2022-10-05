"""arXiv endorsement routes."""

from flask import Blueprint, render_template, Response

blueprint = Blueprint('endorsement', __name__, url_prefix='/endorsement')


@blueprint.route('/request', methods=['GET'])
def display() -> Response:
    """Display a endorsement."""
    return render_template('endorsement/display.html')
