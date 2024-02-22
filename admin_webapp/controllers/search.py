from flask import current_app, Response
from flask_sqlalchemy import Pagination
from admin_webapp.extensions import get_db
from sqlalchemy import select, or_, func
from arxiv_db.models import TapirUsers, TapirNicknames

"""
Searches logic:

"""
def general_search(search_string: str, per_page:int, page: int) -> Response:
    session = get_db(current_app).session

    # check if the string is numeric
    if search_string.isdigit():
        # Check if unique user exists based on user ID
        unique_user_id = session.query(TapirUsers).filter(TapirUsers.user_id==search_string).all()
        if len(unique_user_id) == 1:
            return dict(count=1, unique_id=search_string)
    
    # Check if unique user exists based on nickname
    unique_user_nickname = session.query(TapirNicknames).filter(TapirNicknames.nickname==search_string).all()
    if len(unique_user_nickname) == 1:
        return dict(count=1, unique_id=unique_user_nickname[0].user_id)
    
    # General search logic
    stmt = (select(TapirUsers).join(TapirNicknames)
               .filter(
                   or_(TapirUsers.user_id.like(f'%{search_string}%'),
                       TapirUsers.first_name.like(f'%{search_string}%'),
                        TapirUsers.last_name.like(f'%{search_string}%'),
                        TapirNicknames.nickname.like(f'%{search_string}%')
                       ))
               .limit(per_page).offset((page -1) * per_page))
    
    count_stmt = (select(func.count(TapirUsers.user_id)).where(
        or_(TapirUsers.user_id.like(f'%{search_string}%'),
                       TapirUsers.first_name.like(f'%{search_string}%'),
                        TapirUsers.last_name.like(f'%{search_string}%'),
                        )))

    users = session.scalars(stmt)
    count = session.execute(count_stmt).scalar_one()

    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)

    return dict(pagination=pagination, count=count, users=users)
