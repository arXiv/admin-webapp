"""tapir session routes."""

from flask import Blueprint, render_template, Response

from . import admin_scoped

blueprint = Blueprint('session', __name__, url_prefix='/session')


@blueprint.route('/<int:session_id>', methods=['GET'])
@admin_scoped
def detail(session_id: int) -> Response:
    """Display a session."""
    return render_template('session_display.html')