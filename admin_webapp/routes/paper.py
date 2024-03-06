"""arXiv paper display routes."""

from flask import Blueprint, render_template, Response
from admin_webapp.controllers.document import paper_detail
blueprint = Blueprint('paper', __name__, url_prefix='/paper')


@blueprint.route('/detail/<paper_id>', methods=['GET'])
def detail(paper_id:str) -> Response:
    """Display a paper."""
    return render_template('paper/detail.html', **paper_detail(paper_id))
