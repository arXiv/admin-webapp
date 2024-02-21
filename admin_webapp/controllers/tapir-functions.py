from flask import current_app, Response
from admin_webapp.extensions import get_db
from sqlalchemy import select, func
from arxiv_db.models import TapirEmailTemplates

"""
Searches based on
"""
def manage_email_templates(search_string: str) -> Response:
    session = get_db(current_app).session
    
    stmt = (select(TapirEmailTemplates))
    count_stmt = (select(func.count(TapirEmailTemplates.template_id)))

    email_templates = session.scalars(stmt)
    count = session.execute(count_stmt).scalar_one()

    return dict(count=count, email_templates=email_templates)

    