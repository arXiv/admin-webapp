"""arXiv user routes."""

from flask import Blueprint, render_template, Response


blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/<int:id>', methods=['GET'])
def display() -> Response:
    return render_template('user/display.html')
