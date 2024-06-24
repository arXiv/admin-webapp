"""arXiv paper users controllers."""
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

from arxiv.auth.auth.decorators import scoped
from arxiv.db import session
from arxiv.db.models import (
    TapirUser, Document, ShowEmailRequest, Demographic,
    TapirNickname, TapirAdminAudit, TapirSession, Endorsement, 
    t_arXiv_moderators, t_arXiv_paper_owners)


from .util import Pagination

logger = logging.getLogger(__file__)

# blueprint = Blueprint('ownership', __name__, url_prefix='/ownership')
"""
Get user profile
"""
def user_profile(user_id:int) -> Response:
    stmt = (select(TapirUser)
            .where(
                TapirUser.user_id == user_id
            ))
    print(stmt)
    user = session.scalar(stmt)
    # TODO: optimize this so we can join with the Tapir Users rather than separate query?
    demographics_stmt = (select(Demographic)
                         .where(
                             Demographic.user_id == user_id
                         ))
    demographics = session.scalar(demographics_stmt)

    if not user or not demographics:
        abort(404)
    

    # do a join here with documents
    
    # maybe do a join with sessions too?
    logs = session.query(TapirAdminAudit, Document, TapirSession).filter(TapirAdminAudit.affected_user == user_id).order_by(desc(TapirAdminAudit.log_date))        
    logs = logs.outerjoin(Document, (TapirAdminAudit.data == Document.document_id) & (TapirAdminAudit.action.in_(['add-paper-owner','add-paper-owner-2'])))
    logs = logs.outerjoin(TapirSession, (TapirAdminAudit.data == TapirSession.session_id) & (TapirAdminAudit.action.in_(['become-user',]))).all()
    
    tapir_sessions = session.query(TapirSession).filter(TapirSession.user_id == user_id).order_by(desc(TapirSession.start_time)).all()

    email_request_count = session.query(func.count(func.distinct(ShowEmailRequest.document_id))).filter(ShowEmailRequest.user_id == 123).scalar()

    endorsement_stmt = (select(Endorsement).where(Endorsement.endorsee_id==user_id))
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
    report_stmt = (select(TapirUser)
                #    TODO: do I need a joinedload to prevent N+1 queries
                #    .options(joinedload(TapirUser.tapir_nicknames))
                #    .join(TapirNickname, TapirUser.tapir_nicknames, isouter=True)
                   .filter(TapirUser.policy_class == 1) # admin policy class
                   .limit(per_page).offset((page -1) * per_page))

    count_stmt = (select(func.count(TapirUser.user_id))
                  .where(TapirUser.policy_class == 1))

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
    report_stmt = (select(TapirUser)
                #    TODO: do I need a joinedload to prevent N+1 queries
                #    .options(joinedload(TapirUser.tapir_nicknames))
                   .filter(TapirUser.policy_class == 1) # admin policy class
                   .filter(TapirUser.flag_edit_system == 1)
                   .limit(per_page).offset((page -1) * per_page))

    count_stmt = (select(func.count(TapirUser.user_id))
                  .where(TapirUser.flag_edit_system == 1)
                  .where(TapirUser.policy_class == 1))

    users = session.scalars(report_stmt)
    count = session.execute(count_stmt).scalar_one()
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    return dict(pagination=pagination, count=count, users=users)

def suspect_listing(per_page:int, page: int) -> dict:
    report_stmt = select(TapirUser, func.count(TapirSession.session_id).label('session_count'))\
                    .join(Demographic, Demographic.user_id==TapirUser.user_id)\
                    .filter(Demographic.flag_suspect == "1")\
                    .join(TapirSession, TapirUser.user_id==TapirSession.user_id)\
                    .group_by(TapirUser.user_id)\
                    .limit(per_page).offset((page -1) * per_page)
                    # .subquery()
    
    # report_stmt = select(report_stmt.c.user_id, report_stmt.c.email, func.count())\
    #                .join(TapirSession, report_stmt.c.user_id==TapirSession.user_id)\
    #                .group_by(report_stmt.c.user_id)\
    #                .limit(per_page).offset((page -1) * per_page)
    test_stmt = (select(TapirUser).limit(10))

    report_stmt_sql = "SELECT u.user_id, u.first_name, n.nickname, u.last_name, u.joined_date, u.email, u.flag_email_verified, s.session_count FROM tapir_users u JOIN tapir_nicknames n ON n.user_id = u.user_id  JOIN arXiv_demographics d ON d.user_id = u.user_id  JOIN ( SELECT user_id, COUNT(session_id) AS session_count FROM tapir_sessions GROUP BY user_id ) s ON s.user_id = u.user_id WHERE d.flag_suspect = 1  LIMIT :per_page OFFSET :offset"
    users = session.execute(report_stmt_sql, {"per_page": per_page, "offset": (page -1) * per_page})

    test=session.scalars(test_stmt)
    suspects = select(TapirUser) \
                .join(Demographic) \
                .filter(Demographic.flag_suspect == "1") \
                .subquery()
    
    count = select(func.count()).select_from(suspects)
    count = session.scalar(count)

    # users = session.scalars(report_stmt)
    # users = session.scalars(report_stmt)
    # print(users[0].session_count)
    pagination = Pagination(query=None, page=page, per_page=per_page, total=count, items=None)
    
    return dict(pagination=pagination, count=count, users=users, test=test)


def moderator_listing() -> dict:
    count_stmt = select(func.count(func.distinct(t_arXiv_moderators.c.user_id)))

    # mods = session.scalars(report_stmt)
    mods = (
    session.query(
        t_arXiv_moderators.c.user_id,
        # TODO: Note, is checking for empty string in subject_class enough?
        func.group_concat(func.concat(t_arXiv_moderators.c.archive, case([(t_arXiv_moderators.c.subject_class != '', '.',)], else_=''), t_arXiv_moderators.c.subject_class), order_by=(t_arXiv_moderators.c.archive, t_arXiv_moderators.c.subject_class), separator=', ').label('archive_subject_list'),
        TapirUser,
    )
    .join(TapirUser, t_arXiv_moderators.c.user_id == TapirUser.user_id)
    # .join(TapirNickname, Moderators.user_id == TapirNickname.user_id)

    .group_by(t_arXiv_moderators.c.user_id)
    .order_by(TapirUser.last_name) # order by nickname?
    .all()
    )
    count = session.execute(count_stmt).scalar_one()

    return dict(count=count, mods=mods)

# TODO: optimize this once a relationship between TapirUser and Moderators model is established
def moderator_by_category_listing() -> dict:
    count_stmt = select(func.count(func.distinct(t_arXiv_moderators.c.user_id)))

    mods = (
    session.query(
        t_arXiv_moderators.c.user_id,
        # TODO: Note, is checking for empty string in subject_class enough?
        func.group_concat(func.concat(t_arXiv_moderators.c.archive, case([(t_arXiv_moderators.c.subject_class != '', '.',)], else_=''), t_arXiv_moderators.c.subject_class), order_by=(t_arXiv_moderators.c.archive, t_arXiv_moderators.c.subject_class), separator=', ').label('archive_subject_list'),
        TapirUser
    )
    .join(TapirUser, t_arXiv_moderators.c.user_id == TapirUser.user_id)
    .group_by(t_arXiv_moderators.c.user_id)
    .all()
    )
    count = session.execute(count_stmt).scalar_one()
    mods_map = defaultdict(list)
    mods = sorted(mods, key=lambda x: x[1])
    for mod in mods:
        for pair in mod.archive_subject_list.split(','):
            user = session.scalar((select(TapirUser)
            .where(
                TapirUser.user_id == mod.user_id
            )))
            mods_map[pair].append(user)

    return dict(count=count, mods_map=mods_map)

def add_to_blocked():
    if request.method == 'POST': 
        new_pattern = request.form.get('')
        
    return Response(status=204)

def add_to_approved():
    if request.method == 'POST': 
        new_pattern = request.form.get('')
    
    return Response(status=204)

def non_academic_email_listing():
    blocked_users_all_sql = "create temporary table blocked_users select user_id,email,pattern as black_pattern,joined_date,first_name,last_name,suffix_name from tapir_users,arXiv_black_email where joined_date>UNIX_TIMESTAMP(DATE_SUB(CURDATE(),INTERVAL 30 MONTH)) and email like pattern"
    session.execute(blocked_users_all_sql)
    blocked_users_sql = "select user_id,email,joined_date,black_pattern,first_name,last_name,suffix_name from blocked_users left join arXiv_white_email on email like pattern where pattern is null group by user_id, email, joined_date, black_pattern, first_name, last_name, suffix_name order by joined_date desc"
    blocked_users_sql_len = f"SELECT COUNT(*) FROM ({blocked_users_sql}) as subquery"
   
    blocked_users = session.execute(blocked_users_sql)
    count = session.execute(blocked_users_sql_len)
    return dict(users=blocked_users, count=count)

def flip_email_verified_flag():    
    if request.method == 'POST':
        # do the SQL update here
        verified = request.form.get('emailVerified')
        user_id = request.form.get('user_id')
        if verified == 'on':
            # update the object
            session.execute(update(TapirUser).where(
                TapirUser.user_id==user_id
            ).values(flag_email_verified = 1))
            # update the activity log
        elif not verified:
             session.execute(update(TapirUser).where(
                TapirUser.user_id==user_id
            ).values(flag_email_verified = 0))
    session.commit()
    return Response(status=204)

def flip_bouncing_flag():
    if request.method == 'POST':
        bouncing = request.form.get('bouncing')
        user_id = request.form.get('user_id')
        if bouncing == 'on':
            session.execute(update(TapirUser).where(TapirUser.user_id==user_id).values(email_bouncing = 1))
    
        elif not bouncing: 
            session.execute(update(TapirUser).where(TapirUser.user_id==user_id).values(email_bouncing = 0))
    session.commit()
    return Response(status=204)

def flip_edit_users_flag():
    if request.method == 'POST':
        edit_users = request.form.get('editUsers')
        user_id = request.form.get('user_id')
        if edit_users == 'on':
            session.execute(update(TapirUser).where(TapirUser.user_id==user_id).values(flag_edit_users = 1))
    
        elif not edit_users:
            session.execute(update(TapirUser).where(TapirUser.user_id==user_id).values(flag_edit_users = 0))
    session.commit()
    return Response(status=204)
    
def flip_edit_system_flag():
    if request.method == 'POST':
        edit_system = request.form.get('editSystem')
        user_id = request.form.get('user_id')
        if edit_system == 'on':
            session.execute(update(TapirUser).where(TapirUser.user_id==user_id).values(flag_edit_system = 1))
        elif not edit_system:
            session.execute(update(TapirUser).where(TapirUser.user_id==user_id).values(flag_edit_system = 0))
    session.commit()
    return Response(status=204)

def flip_proxy_flag():
    if request.method == 'POST': 
        print('post')
    
    return Response(status=204)

# wip flags
def flip_suspect_flag():
    if request.method == 'POST': 
        print('post')
    
    return Response(status=204)

def flip_next_flag():
    if request.method == 'POST': 
        print('post')
    
    return Response(status=204)
