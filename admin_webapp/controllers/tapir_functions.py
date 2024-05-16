from flask import current_app, Response, request
from admin_webapp.extensions import get_db
from sqlalchemy import select, func, insert
from arxiv_db.models import TapirEmailTemplates
from datetime import datetime

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

def edit_email_template(template_id: int) -> Response:
    session = get_db(current_app).session
    stmt = (select(TapirEmailTemplates).where(TapirEmailTemplates.template_id == template_id))
    template = session.scalar(stmt)
    
    return dict(template=template)

def create_email_template() -> Response:
    session = get_db(current_app).session
    if request.method == 'POST':
        short_name = request.form.get('shortName')
        long_name = request.form.get('longName')
        template_data = request.form.get('templateData')
    
        # incomplete list 
        stmt = insert(TapirEmailTemplates).values(
            short_name=short_name, 
            long_name=long_name, 
            update_date=int(datetime.now().astimezone(current_app.config['ARXIV_BUSINESS_TZ']).timestamp()),
            workflow_status=2,
            data=template_data   
        )
        session.execute(stmt)
    session.commit()
    return
