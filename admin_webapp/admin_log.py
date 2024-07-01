from datetime import datetime
from typing import Literal, Union

from admin_webapp.extensions import get_db

from flask import current_app, request


from arxiv.db.models import TapirAdminAudit


Actions = Literal['new-user',
                  'change-password',
                  'become-user',  # data = new session id
                  'add-paper-owner-2',  #data = document_id
                  ]

def audit_admin(affected_user:int, action:Actions, data="", comment=""):
    """Creates a tapir_admin_audit row.

    Does not call commit.
    """
    session = get_db(current_app)

    item=TapirAdminAudit(log_date=int(datetime.now().astimezone(current_app.config['ARXIV_BUSINESS_TZ']).timestamp()),
                         ip_addr = request.remote_addr,
                         affected_user=affected_user,
                         tracking_cookie=request.cookies.get(current_app.config['AUTH_SESSION_COOKIE_NAME'], ''),
                         action=action,
                         data=data,
                         comment=comment,
                         session_id=request.auth.session_id,
                         admin_user=request.auth.user.user_id,
                    )
    session.add(item)
