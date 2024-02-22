from flask import current_app, Response
from admin_webapp.extensions import get_db
from sqlalchemy import select, func
from arxiv_db.models import TapirEmailTemplates
import json 

"""
Tapir email templates
"""
def manage_email_templates() -> Response:
    session = get_db(current_app).session
    
    stmt = (select(TapirEmailTemplates))
    count_stmt = (select(func.count(TapirEmailTemplates.template_id)))

    email_templates = session.scalars(stmt)
    count = session.execute(count_stmt).scalar_one()

    # return json.dumps(email_templates)
    return dict(count=count, email_templates=email_templates)

def email_template(template_id: int) -> Response:
    session = get_db(current_app).session

    stmt = (select(TapirEmailTemplates).where(TapirEmailTemplates.template_id == template_id))
    
    template = session.scalar(stmt)

    return dict(template=template)