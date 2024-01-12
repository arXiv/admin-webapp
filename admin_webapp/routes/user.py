"""arXiv user routes."""

from flask import Blueprint, render_template, Response, request

from admin_webapp.controllers.users import administrator_listing, administrator_edit_sys_listing, suspect_listing, user_profile

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/<int:user_id>', methods=['GET'])
def display(user_id:int) -> Response:
    """Display a user."""
    return render_template('user/display.html', **user_profile(user_id))

# perhaps we need to scope this?
@blueprint.route('/administrators', methods=['GET'])
def administrators() -> Response:
    """
    Show administrators view
    """
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)    
    
    data = administrator_listing(per_page, page)
    data['title'] = "Administrators"
    return render_template('user/list.html', **data)

# perhaps we need to scope this?
@blueprint.route('/administrators/sys', methods=['GET'])
def administrators_sys() -> Response:
    """
    Show administrators view
    """
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)    
    
    data = administrator_edit_sys_listing(per_page, page)
    data['title'] = "Administrators"
    return render_template('user/list.html', **data)


# perhaps we need to scope this?
@blueprint.route('/suspects', methods=['GET'])
def suspects() -> Response:
    """
    Show administrators view
    """
    args = request.args
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)    
    
    data = suspect_listing(per_page, page)
    data['title'] = "Suspects"
    return render_template('user/list.html', **data)
