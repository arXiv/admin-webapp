"""arXiv user routes."""

from flask import Blueprint, render_template, Response, request, redirect

from admin_webapp.controllers.users import administrator_listing, administrator_edit_sys_listing, suspect_listing, user_profile, moderator_listing, moderator_by_category_listing, flip_email_verified_flag, flip_bouncing_flag, flip_edit_users_flag, flip_edit_system_flag, non_academic_email_listing
from admin_webapp.controllers.search import general_search

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/<int:user_id>', methods=['GET'])
def display(user_id:int) -> Response:
    """Display a user."""
    if request.method == 'GET':
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

@blueprint.route('/moderators', methods=['GET'])
def moderators() -> Response:
    """
    Show moderators view
    No pagination
    """
    args = request.args
    data = moderator_listing()
    data['title'] = "Moderators"
    return render_template('user/moderators.html', **data)

@blueprint.route('/moderators_by_category', methods=['GET'])
def moderators_by_category() -> Response:
    """
    Show moderators by category view
    No pagination
    """
    args = request.args
    data = moderator_by_category_listing()
    data['title'] = "Moderators"
    return render_template('user/moderators_by_category.html', **data)

@blueprint.route('/non_academic_emails', methods=['GET'])
def non_academic_emails() -> Response:
    """
    Show users with non-academic emails
    """
    args = request.args
    data = non_academic_email_listing()
    data['title'] = "Non-academic Emails"
    return render_template('user/non_academic_emails.html', **data)

@blueprint.route('/search', methods=['GET', 'POST'])
def search() -> Response:
    args = request.args
    term = args.get('search')
    per_page = args.get('per_page', default=12, type=int)
    page = args.get('page', default=1, type=int)    
    
    data = general_search(term, per_page, page)
    if data['count'] == 1:
        return redirect('/user/' + str(data['unique_id']))
    return render_template('user/list.html', **data)

@blueprint.route('/flip/email_verified', methods=['POST'])
def flip_email_verified() -> Response:
    return flip_email_verified_flag()

@blueprint.route('/flip/bouncing', methods=['POST'])
def flip_bouncing() -> Response:
    return flip_bouncing_flag()

@blueprint.route('flip/edit_users', methods=['POST'])
def flip_edit_users() -> Response: 
    return flip_edit_users_flag()

@blueprint.route('flip/edit_system', methods=['POST'])
def flip_edit_system() -> Response:
    return flip_edit_system_flag()