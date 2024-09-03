"""arXiv moderator routes."""
import re
from datetime import timedelta, datetime, date
from enum import Enum
import urllib.parse
from typing import Optional, List, Any

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Response

from sqlalchemy import select, update, func, case, Select, distinct, exists, and_
from sqlalchemy.orm import Session, joinedload

from pydantic import BaseModel, Field
from arxiv.base import logging
from arxiv.db import transaction
from arxiv.db.models import t_arXiv_moderators, TapirUser

from . import is_admin_user, get_db, datetime_to_epoch, VERY_OLDE

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/moderators")


class ModeratorModel(BaseModel):
    id: str
    user_id: int
    archive: str
    subject_class: Optional[str]
    is_public: bool
    no_email: bool
    no_web_email: bool
    no_reply_to: bool
    daily_update: bool

    class Config:
        orm_mode = True

    @classmethod
    def base_query(cls, db: Session) -> Query:
        return db.query(
            func.concat(t_arXiv_moderators.c.user_id, "+",
                        t_arXiv_moderators.c.archive, "+",
                        t_arXiv_moderators.c.subject_class).label("id"),
            t_arXiv_moderators.c.user_id,
            t_arXiv_moderators.c.archive,
            t_arXiv_moderators.c.subject_class,
            t_arXiv_moderators.c.is_public,
            t_arXiv_moderators.c.no_email,
            t_arXiv_moderators.c.no_web_email,
            t_arXiv_moderators.c.no_reply_to,
            t_arXiv_moderators.c.daily_update,
        )


@router.get('/')
async def list_moderators_0(
        response: Response,
        _sort: Optional[str] = Query("archive,subject_class", description="keys"),
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        user_id: Optional[int] = Query(None),
        archive: Optional[str] = Query(None),
        subject_class: Optional[str] = Query(None),
        first_name: Optional[str] = Query(None),
        last_name: Optional[str] = Query(None),
        db: Session = Depends(get_db)
    ) -> List[ModeratorModel]:
    if _start < 0 or _end < _start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start or end index")

    order_columns = []
    if _sort:
        keys = _sort.split(",")
        for key in keys:
            if key in order_columns:
                continue
            if key == "id":
                order_columns = [
                    getattr(t_arXiv_moderators.c, col) for col in ["archive", "subject_class", "user_id"]
                ]
                continue
            try:
                order_column = getattr(t_arXiv_moderators.c, key)
                order_columns.append(order_column)
            except AttributeError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid start or end index")

    query = ModeratorModel.base_query(db)
    if user_id is not None:
        query = query.filter(t_arXiv_moderators.c.user_id == user_id)

    if archive is not None:
        query = query.filter(t_arXiv_moderators.c.archive.ilike(archive + "%"))

    if subject_class is not None:
        query = query.filter(t_arXiv_moderators.c.subject_class.ilike(subject_class + "%"))

    if first_name is not None and last_name is not None:
        query = query.join(
            TapirUser,
            and_(
                TapirUser.user_id == t_arXiv_moderators.c.user_id,
                TapirUser.first_name.ilike(first_name + "%"),
                TapirUser.last_name.ilike(last_name + "%"),
            ))
    elif first_name is not None:
        query = query.join(
            TapirUser,
            and_(
                TapirUser.user_id == t_arXiv_moderators.c.user_id,
                TapirUser.first_name.ilike(first_name + "%"),
            ))
    elif last_name is not None:
        query = query.join(
            TapirUser,
            and_(
                TapirUser.user_id == t_arXiv_moderators.c.user_id,
                TapirUser.last_name.ilike(last_name + "%"),
            ))

    for column in order_columns:
        if _order == "DESC":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    return [ModeratorModel.from_orm(mod) for mod in query.offset(_start).limit(_end - _start).all()]


@router.get('/{archive}/subject-class')
async def list_moderators_1(
        response: Response,
        archive: str,
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        db: Session = Depends(get_db)
    ) -> List[ModeratorModel]:
    if _start < 0 or _end < _start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start or end index")

    query = ModeratorModel.base_query(db).filter(t_arXiv_moderators.c.archive == archive)

    if _order == "DESC":
        query = query.order_by(t_arXiv_moderators.c.subject_class.desc())
    else:
        query = query.order_by(t_arXiv_moderators.c.subject_class.asc())

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    return [ModeratorModel.from_orm(mod) for mod in query.offset(_start).limit(_end - _start).all()]


@router.get('/{archive}/subject-class/{subject_class}')
async def list_moderators_2(
        response: Response,
        archive: str,
        subject_class: str,
        db: Session = Depends(get_db)
    ) -> List[ModeratorModel]:
    query = ModeratorModel.base_query(db).filter(
        and_(
            t_arXiv_moderators.c.archive == archive,
            t_arXiv_moderators.c.subject_class == subject_class)
    )
    count = query.count()
    response.headers['X-Total-Count'] = count
    return [ModeratorModel.from_orm(row) for row in query.all()]


@router.get('/{id:str}')
async def get_moderator(id: str, db: Session = Depends(get_db)) -> ModeratorModel:
    [user_id, archive, subject_class] = id.split("+")
    id = int(user_id)
    mod = ModeratorModel.base_query(db).filter(
        and_(
            t_arXiv_moderators.c.user_id == id,
            t_arXiv_moderators.c.archive == archive,
            t_arXiv_moderators.c.subject_class == subject_class
        )).one_or_none()
    if mod:
        return ModeratorModel.from_orm(mod)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id:str}')
async def update_moderator(request: Request, id: str,
                           session: Session = Depends(transaction)) -> ModeratorModel:
    body = await request.json()
    [user_id, archive, subject_class] = id.split("+")
    item = ModeratorModel.base_query(session).filter(
        and_(
            t_arXiv_moderators.c.user_id == int(user_id),
            t_arXiv_moderators.c.archive == archive,
            t_arXiv_moderators.c.subject_class == subject_class)).one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify?
    for key, value in body.items():
        if key in item.__dict__:
            setattr(item, key, value)

    session.commit()
    session.refresh(item)  # Refresh the instance with the updated data
    return ModeratorModel.from_orm(item)


@router.post('/')
async def create_moderator(
        request: Request,
        session: Session = Depends(transaction)) -> ModeratorModel:
    body = await request.json()

    item = t_arXiv_moderators(**body)
    session.add(item)
    session.commit()
    session.refresh(item)
    return ModeratorModel.from_orm(item)


@router.delete('/{id:str}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_moderator(id: str, session: Session = Depends(transaction)) -> Response:
    [user_id, archive, subject_class] = id.split("+")
    item = session.query(t_arXiv_moderators).filter(
        and_(
            t_arXiv_moderators.c.user_id == user_id,
            t_arXiv_moderators.c.archive == archive,
            t_arXiv_moderators.c.subject_class == subject_class)).one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Moderator not found")

    item.delete_instance()
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
