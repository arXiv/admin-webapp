"""arXiv user routes."""
from http.client import HTTPException
from typing import Optional, List, Any
from datetime import datetime

from fastapi import APIRouter, Query, HTTPException, status, Depends, Request
from fastapi.responses import Response

from sqlalchemy import select, update, func, case, Select, distinct, exists
from sqlalchemy.orm import Session, aliased

from pydantic import BaseModel

from arxiv.db import transaction
from arxiv.db.models import TapirUser, TapirNickname, t_arXiv_moderators, Demographic, TapirCountry


from .models import DemographicModel

from . import is_admin_user, get_db

router = APIRouter(dependencies=[Depends(is_admin_user)], prefix="/users")

class UserModel(BaseModel):
    class Config:
        orm_mode = True
    id: int
    email: str
    first_name: str
    last_name: str
    suffix_name: str
    username: str
    email_bouncing: bool
    policy_class:  int
    joined_date:  datetime
    joined_remote_host: str
    flag_internal:  bool
    flag_edit_users: bool
    flag_edit_system:  bool
    flag_email_verified:  bool
    flag_approved:  bool
    flag_deleted:  bool
    flag_banned:  bool
    flag_wants_email:  Optional[bool]
    flag_html_email:  Optional[bool]
    flag_allow_tex_produced:  Optional[bool]
    flag_can_lock:  Optional[bool]
    flag_is_mod: Optional[bool]

    flag_suspect: Optional[bool]
    dirty: Optional[int]  # 0, 1, 2
    moderator_id: Optional[str]

    @staticmethod
    def base_select(db: Session):
        is_mod_subquery = exists().where(t_arXiv_moderators.c.user_id == TapirUser.user_id).correlate(TapirUser)
        nick_subquery = select(TapirNickname.nickname).where(TapirUser.user_id == TapirNickname.user_id).correlate(TapirUser).limit(1).scalar_subquery()
        """
        mod_subquery = select(
            func.concat(t_arXiv_moderators.c.user_id, "+",
                        t_arXiv_moderators.c.archive, "+",
                        t_arXiv_moderators.c.subject_class)
        ).where(t_arXiv_moderators.c.user_id == TapirUser.user_id).correlate(TapirUser)
        """

        return (db.query(
            TapirUser.user_id.label("id"),
            TapirUser.email,
            TapirUser.first_name,
            TapirUser.last_name,
            TapirUser.suffix_name,
            nick_subquery.label("username"),
            TapirUser.email_bouncing,
            TapirUser.policy_class,
            TapirUser.joined_date,
            TapirUser.joined_remote_host,
            TapirUser.flag_internal,
            TapirUser.flag_edit_users,
            TapirUser.flag_edit_system,
            TapirUser.flag_email_verified,
            TapirUser.flag_approved,
            TapirUser.flag_deleted,
            TapirUser.flag_banned,
            TapirUser.flag_wants_email,
            TapirUser.flag_html_email,
            TapirUser.flag_allow_tex_produced,
            TapirUser.flag_can_lock,
            case(
                (is_mod_subquery, True),  # Pass each "when" condition as a separate positional argument
                else_=False
            ).label("flag_is_mod"),
            Demographic.flag_suspect.label('flag_suspect'),
            Demographic.dirty,
            # mod_subquery.label("moderator_id"),
            )
                .outerjoin(Demographic, TapirUser.user_id == Demographic.user_id)
                # .outerjoin(t_arXiv_moderators, TapirUser.user_id == t_arXiv_moderators.c.user_id)
                )

    pass


@router.get("/{user_id:int}")
def get_one_user(user_id:int, db: Session = Depends(get_db)) -> UserModel:
    user = UserModel.base_select(db).filter(TapirUser.user_id == user_id).one_or_none()
    if user:
        return UserModel.from_orm(user)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/")
async def list_users(
        response: Response,
        _sort: Optional[str] = Query("last_name,first_name", description="sort by"),
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        user_class: Optional[str] = Query(None, description="None for all, 'admin|owner'"),
        flag_is_mod: Optional[bool] = Query(None, description="moderator"),
        is_non_academic: Optional[bool] = Query(None, description="non-academic"),
        username: Optional[str] = Query(None),
        email: Optional[str] = Query(None),
        last_name: Optional[str] = Query(None),
        first_name: Optional[str] = Query(None),
        flag_edit_users: Optional[bool] = Query(None),
        flag_email_verified: Optional[bool] = Query(None),
        email_bouncing: Optional[bool] = Query(None),
        suspect: Optional[bool] = Query(None),
        id: Optional[List[int]] = Query(None, description="List of user IDs to filter by"),
        db: Session = Depends(get_db)
) -> List[UserModel]:
    """
    List users
    """
    if _start < 0 or _end < _start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start or end index")

    order_columns = []
    if _sort:
        keys = _sort.split(",")
        for key in keys:
            if key == "id":
                key = "user_id"
            try:
                order_column = getattr(TapirUser, key)
                order_columns.append(order_column)
            except AttributeError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid start or end index")

    query = UserModel.base_select(db)

    if id is not None:
        query = query.filter(TapirUser.user_id.in_(id))

    if suspect:
        dgfx = aliased(Demographic)
        query = query.join(dgfx, dgfx.user_id == TapirUser.user_id)
        query = query.filter(dgfx.flag_suspect == suspect)

    if user_class in ["owner", "admin"]:
        query = query.filter(TapirUser.policy_class == False)

    if user_class in ["owner"]:
        query = query.filter(TapirUser.flag_edit_system == True)

    if flag_edit_users is not None:
        query = query.filter(TapirUser.flag_edit_users == flag_edit_users)

    if flag_is_mod is not None:
        subquery = select(distinct(t_arXiv_moderators.c.user_id))
        if flag_is_mod:
            # I think this is faster but I cannot make it work...
            # query = query.join(t_arXiv_moderators, TapirUser.user_id == t_arXiv_moderators.c.user_id)
            query = query.filter(TapirUser.user_id.in_(subquery))
        else:
            query = query.filter(~TapirUser.user_id.in_(subquery))

    if username:
        query = query.filter(TapirUser.tapir_nicknames.contains(username))

    if first_name:
        query = query.filter(TapirUser.first_name.contains(first_name))

    if last_name:
        query = query.filter(TapirUser.last_name.contains(last_name))

    if email:
        query = query.filter(TapirUser.email.contains(email))

    if flag_email_verified is not None:
        query = query.filter(TapirUser.flag_email_verified == flag_email_verified)

    if email_bouncing is not None:
        query = query.filter(TapirUser.email_bouncing == email_bouncing)

    for column in order_columns:
        if _order == "DESC":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    result = [UserModel.from_orm(user) for user in query.offset(_start).limit(_end - _start).all()]
    return result


@router.put('/{user_id:int}')
async def update_user(request: Request, user_id: int, session: Session = Depends(transaction)) -> UserModel:
    """Update user - by PUT"""
    body = await request.json()

    user = session.query(TapirUser).filter(TapirUser.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify?
    for key, value in body.items():
        if key in user.__dict__:
            setattr(user, key, value)

    session.commit()
    session.refresh(user)  # Refresh the instance with the updated data
    return UserModel.from_orm(user)


@router.post('/')
async def create_user(request: Request, session: Session = Depends(transaction)) -> UserModel:
    """Creates a new user - by POST"""
    body = await request.json()

    user = TapirUser()
    for key, value in body.items():
        if key in user.__dict__:
            setattr(user, key, value)
    session.add(user)
    return UserModel.from_orm(user)


@router.delete('/{user_id:int}')
def delete_user(user_id: int, session: Session = Depends(transaction)) -> UserModel:
    user: TapirUser = session.query(TapirUser).filter(TapirUser.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.flag_deleted = True

    session.commit()
    session.refresh(user)  # Refresh the instance with the updated data
    return UserModel.from_orm(user)
