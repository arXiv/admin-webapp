"""arXiv session routes."""

from flask import Blueprint, render_template, Response


blueprint = Blueprint('session', __name__, url_prefix='/session')


@blueprint.route('/<int:session_id>', methods=['GET'])
def detail(session_id: int) -> Response:
    """Display a session."""
    return render_template('session_display.html')
