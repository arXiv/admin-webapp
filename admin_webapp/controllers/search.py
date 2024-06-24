from flask import current_app, Response
from sqlalchemy import select, or_, func
from arxiv.db import session
from arxiv.db.models import TapirUser, TapirNickname

from .util import Pagination

"""
Basic search logic that does some loose similarity checking:

"""
def general_search(search_string: str, per_page:int, page: int) -> Response:
    # check if the string is numeric
    if search_string.isdigit():
        # Check if unique user exists based on user ID
        unique_user_id = session.query(TapirUser).filter(TapirUser.user_id==search_string).all()
        if len(unique_user_id) == 1:
            return dict(count=1, unique_id=search_string)
    
    # Check if unique user exists based on nickname
    unique_user_nickname = session.query(TapirNickname).filter(TapirNickname.nickname==search_string).all()
    if len(unique_user_nickname) == 1:
        return dict(count=1, unique_id=unique_user_nickname[0].user_id)
    
    # General search logic
    stmt = (select(TapirUser).join(TapirNickname)
               .filter(
                   or_(TapirUser.user_id.like(f'%{search_string}%'),
                       TapirUser.first_name.like(f'%{search_string}%'),
                        TapirUser.last_name.like(f'%{search_string}%'),
                        TapirNickname.nickname.like(f'%{search_string}%')
                       ))
               .limit(per_page).offset((page -1) * per_page))
    
    count_stmt = (select(func.count(TapirUser.user_id)).where(
        or_(TapirUser.user_id.like(f'%{search_string}%'),
                       TapirUser.first_name.like(f'%{search_string}%'),
                        TapirUser.last_name.like(f'%{search_string}%'),
                        )))

    users = session.scalars(stmt)
    count = session.execute(count_stmt).scalar_one()

    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)

    return dict(pagination=pagination, count=count, users=users)

def advanced_search(options):
    return