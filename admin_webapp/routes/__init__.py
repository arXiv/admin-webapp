"""Contains route information."""
from typing import Dict

from sqlalchemy.sql import select, exists

from arxiv.auth.auth.decorators import scoped
from arxiv.db import session as db_session
from arxiv.db.models import TapirUser

def _is_admin (session: Dict, *args, **kwargs) -> bool:
    try:
        uid = session.user.user_id
    except:
        return False
    return db_session.scalar(
        select(TapirUser)
        .filter(TapirUser.flag_edit_users == 1)
        .filter(TapirUser.user_id == uid)) is not None

admin_scoped = scoped(
    required=None,
    resource=None,
    authorizer=_is_admin,
    unauthorized=None
)