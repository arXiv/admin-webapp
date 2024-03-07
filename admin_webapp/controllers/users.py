"""arXiv paper users controllers."""
from collections import defaultdict
from datetime import datetime, timedelta
import logging
from admin_webapp.routes import endorsement

from flask import Blueprint, render_template, request, \
    make_response, current_app, Response, abort

from flask_sqlalchemy import Pagination

from sqlalchemy import select, func, case, text, insert, update, desc
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import joinedload, selectinload, aliased
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped

from admin_webapp.models import Moderators

from arxiv_db.models import TapirUsers, Documents, ShowEmailRequests, Demographics, TapirNicknames, TapirAdminAudit, TapirSessions, Endorsements
from arxiv_db.models.associative_tables import t_arXiv_paper_owners

from admin_webapp.extensions import get_csrf, get_db
from admin_webapp.admin_log import audit_admin
logger = logging.getLogger(__file__)

# blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')
"""
Get user profile
"""
def user_profile(user_id:int) -> Response:
    session = get_db(current_app).session
    stmt = (select(TapirUsers)
            .where(
                TapirUsers.user_id == user_id
            ))
    user = session.scalar(stmt)
    # TODO: optimize this so we can join with the Tapir Users rather than separate query?
    demographics_stmt = (select(Demographics)
                         .where(
                             Demographics.user_id == user_id
                         ))
    demographics = session.scalar(demographics_stmt)

    if not user or not demographics:
        abort(404)
    

    # do a join here with documents
    
    # maybe do a join with sessions too?
    logs = session.query(TapirAdminAudit, Documents, TapirSessions).filter(TapirAdminAudit.affected_user == user_id).order_by(desc(TapirAdminAudit.log_date))        
    logs = logs.outerjoin(Documents, (TapirAdminAudit.data == Documents.document_id) & (TapirAdminAudit.action.in_(['add-paper-owner','add-paper-owner-2'])))
    logs = logs.outerjoin(TapirSessions, (TapirAdminAudit.data == TapirSessions.session_id) & (TapirAdminAudit.action.in_(['become-user',]))).all()
    
    tapir_sessions = session.query(TapirSessions).filter(TapirSessions.user_id == user_id).order_by(desc(TapirSessions.start_time)).all()

    email_request_count = session.query(func.count(func.distinct(ShowEmailRequests.document_id))).filter(ShowEmailRequests.user_id == 123).scalar()

    endorsement_stmt = (select(Endorsements).where(Endorsements.endorsee_id==user_id))
    endorsements = session.scalars(endorsement_stmt)

    has_endorsed_sql = "select endorsement_id,archive,endorsee_id,nickname,archive,subject_class,arXiv_endorsements.flag_valid,type,point_value from arXiv_endorsements left join tapir_nicknames on (endorsee_id=user_id AND flag_primary=1) where endorser_id=:user_id order by archive,subject_class"
    has_endorsed = session.execute(has_endorsed_sql, {"user_id": user_id})

    papers_sql = "SELECT d.document_id,d.paper_id,m.title AS metadata_title,d.authors,d.submitter_id,flag_author,valid FROM arXiv_documents d JOIN arXiv_paper_owners po ON po.document_id=d.document_id JOIN arXiv_metadata m ON m.document_id=d.document_id WHERE po.user_id=:user_id AND m.is_current=1 ORDER BY dated DESC"
    papers_sql_len = f"SELECT COUNT(*) FROM ({papers_sql}) as subquery"
    papers = session.execute(papers_sql, {"user_id": user_id})
    papers_len = session.execute(papers_sql_len, {"user_id": user_id})

    data = dict(user=user, 
                demographics=demographics, 
                logs=logs, 
                sessions=tapir_sessions, 
                email_request_count=email_request_count, 
                endorsements=endorsements,
                has_endorsed=has_endorsed, 
                papers=papers, 
                papers_len=papers_len.fetchone()[0])
    
    return data


def administrator_listing(per_page:int, page: int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(TapirUsers)
                #    TODO: do I need a joinedload to prevent N+1 queries
                #    .options(joinedload(TapirUsers.tapir_nicknames))
                #    .join(TapirNicknames, TapirUsers.tapir_nicknames, isouter=True)
                   .filter(TapirUsers.policy_class == 1) # admin policy class
                   .limit(per_page).offset((page -1) * per_page))

    count_stmt = (select(func.count(TapirUsers.user_id))
                  .where(TapirUsers.policy_class == 1))

    # if workflow_status in ('accepted', 'rejected'):
    #     window = datetime.now() - timedelta(days=days_back)
    #     report_stmt = report_stmt.join(OwnershipRequestsAudit).filter( OwnershipRequestsAudit.date > window)
    #     count_stmt = count_stmt.join(OwnershipRequestsAudit).filter(OwnershipRequestsAudit.date > window)

    users = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    # why does this prevent print out ?

    return dict(pagination=pagination, count=count, users=users)

def administrator_edit_sys_listing(per_page:int, page: int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(TapirUsers)
                #    TODO: do I need a joinedload to prevent N+1 queries
                #    .options(joinedload(TapirUsers.tapir_nicknames))
                   .filter(TapirUsers.policy_class == 1) # admin policy class
                   .filter(TapirUsers.flag_edit_system == 1)
                   .limit(per_page).offset((page -1) * per_page))

    count_stmt = (select(func.count(TapirUsers.user_id))
                  .where(TapirUsers.flag_edit_system == 1)
                  .where(TapirUsers.policy_class == 1))

    users = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, users=users)


# TODO: this is broken because of a faulty TapirUser-Demographic relationship
def suspect_listing(per_page:int, page: int) -> dict:
    session = get_db(current_app).session
    report_stmt = (select(TapirUsers)
                   .options(joinedload(TapirUsers.demographics))
                   .filter(Demographics.flag_suspect == "1")
                   .limit(per_page).offset((page -1) * per_page))

    count_stmt = (select(func.count(TapirUsers.user_id))
                  .where(Demographics.flag_suspect == "1"))

    users = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, users=users)


def moderator_listing() -> dict:
    session = get_db(current_app).session

    count_stmt = select(func.count(func.distinct(Moderators.user_id)))

    # mods = session.scalars(report_stmt)
    mods = (
    session.query(
        Moderators.user_id,
        # TODO: Note, is checking for empty string in subject_class enough?
        func.group_concat(func.concat(Moderators.archive, case([(Moderators.subject_class != '', '.',)], else_=''), Moderators.subject_class), order_by=(Moderators.archive, Moderators.subject_class), separator=', ').label('archive_subject_list'),
        TapirUsers,
    )
    .join(TapirUsers, Moderators.user_id == TapirUsers.user_id)
    # .join(TapirNicknames, Moderators.user_id == TapirNicknames.user_id)

    .group_by(Moderators.user_id)
    .order_by(TapirUsers.last_name) # order by nickname?
    .all()
    )
    count = session.execute(count_stmt).scalar_one()

    return dict(count=count, mods=mods)

# TODO: optimize this once a relationship between TapirUsers and Moderators model is established
def moderator_by_category_listing() -> dict:
    session = get_db(current_app).session

    count_stmt = select(func.count(func.distinct(Moderators.user_id)))

    mods = (
    session.query(
        Moderators.user_id,
        # TODO: Note, is checking for empty string in subject_class enough?
        func.group_concat(func.concat(Moderators.archive, case([(Moderators.subject_class != '', '.',)], else_=''), Moderators.subject_class), order_by=(Moderators.archive, Moderators.subject_class), separator=', ').label('archive_subject_list'),
        TapirUsers
    )
    .join(TapirUsers, Moderators.user_id == TapirUsers.user_id)
    .group_by(Moderators.user_id)
    .all()
    )
    count = session.execute(count_stmt).scalar_one()
    mods_map = defaultdict(list)
    mods = sorted(mods, key=lambda x: x[1])
    for mod in mods:
        for pair in mod.archive_subject_list.split(','):
            user = session.scalar((select(TapirUsers)
            .where(
                TapirUsers.user_id == mod.user_id
            )))
            mods_map[pair].append(user)

    return dict(count=count, mods_map=mods_map)

