"""arXiv endorsement routes."""

from flask import Blueprint, render_template, Response, request
from admin_webapp.controllers.endorsement import endorsement_listing

blueprint = Blueprint('endorsement', __name__, url_prefix='/endorsement')

@blueprint.route('/all', methods=['GET'])
def endorsements() -> Response:
    """
    Show administrators view
    """
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)
    
    data = endorsement_listing(per_page, page)
    data['title'] = "Endorsements"
    return render_template('endorsement/list.html', **data)

@blueprint.route('/request', methods=['GET'])
def request_detail() -> Response:
    """Display a endorsement."""
    return render_template('endorsement/display.html')

@blueprint.route('/modify', methods=['GET'])
def modify_form() -> Response:
    """Modify lists"""
    return render_template('endorsement/modify.html')
