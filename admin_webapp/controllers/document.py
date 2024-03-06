from collections import defaultdict
from datetime import datetime, timedelta
import logging
from admin_webapp.routes import endorsement

from flask import Blueprint, render_template, request, \
    make_response, current_app, Response, abort

from sqlalchemy import select, func, case, text, insert, update, desc
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import joinedload, selectinload, aliased
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped

from arxiv_db.models import Documents, Metadata, PaperPw, AdminLog
from arxiv_db.models.associative_tables import t_arXiv_paper_owners

from admin_webapp.extensions import get_csrf, get_db
from admin_webapp.admin_log import audit_admin
logger = logging.getLogger(__file__)

def paper_detail(doc_id:int) -> Response:
    session = get_db(current_app).session
    doc_stmt = (select(Documents).where(Documents.document_id == doc_id))
    sub_history_stmt = (select(Metadata).where(Metadata.document_id==doc_id).order_by(desc(Metadata.version)))
    doc_pw_stmt = (select(PaperPw).where(PaperPw.document_id == doc_id))
    admin_log_stmt = (select(AdminLog).where(AdminLog.document_id == doc_id))

    document = session.scalar(doc_stmt)
    doc_pw = session.scalar(doc_pw_stmt)
    sub_history = session.scalars(sub_history_stmt)
    # admin_log = session.scalars(admin_log_stmt)
    
    
    admin_log_sql = "SELECT created,submission_id,paper_id,username,program,command,logtext FROM arXiv_admin_log WHERE paper_id=:paper_id UNION DISTINCT SELECT arXiv_admin_log.created AS created,arXiv_admin_log.submission_id AS submission_id,paper_id,username,program,command,logtext FROM arXiv_admin_log,arXiv_submissions WHERE arXiv_submissions.submission_id=arXiv_admin_log.submission_id AND doc_paper_id=:paper_id ORDER BY created DESC"
    admin_log_sql_len = f"SELECT COUNT(*) FROM ({admin_log_sql}) as subquery"
    admin_log = session.execute(admin_log_sql,  {"paper_id": document.paper_id})
    
    admin_log_len = session.execute(admin_log_sql_len, {"paper_id": document.paper_id})
    data = dict(document=document, doc_pw=doc_pw, sub_history=sub_history, admin_log=admin_log, admin_log_len=admin_log_len.fetchone()[0])
    
    return data

