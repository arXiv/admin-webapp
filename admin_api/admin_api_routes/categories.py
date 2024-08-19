"""arXiv category routes."""
import re
from datetime import timedelta, datetime, date
from enum import Enum
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Response

from sqlalchemy import select, update, func, case, Select, distinct, exists, and_
from sqlalchemy.orm import Session, joinedload

from pydantic import BaseModel, Field
from arxiv.base import logging
from arxiv.db import transaction
from arxiv.db.models import Category

from . import is_admin_user, get_db, datetime_to_epoch, VERY_OLDE
from .models import CategoryModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/categories")

class EndorseOption(str, Enum):
    y = 'y'
    n = 'n'
    d = 'd'


class ArchiveModel(BaseModel):
    id: str
    name: str
    description: str

class SubjectClassModel(BaseModel):
    id: str
    name: str
    description: str

@router.get('/')
async def list_categories(
        response: Response,
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        db: Session = Depends(get_db)
    ) -> List[ArchiveModel]:
    if _start < 0 or _end < _start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start or end index")

    query = db.query(Category.archive).distinct()

    if _order == "DESC":
        query = query.order_by(Category.archive.desc())
    else:
        query = query.order_by(Category.archive.asc())

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    return [{"id": cat.archive, "name": cat.archive, "description": cat.archive} for cat in query.offset(_start).limit(_end - _start).all()]


@router.get('/{archive}/subject-class')
async def list_subject_classes(
        response: Response,
        archive: str,
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        db: Session = Depends(get_db)
    ) -> List[SubjectClassModel]:
    if _start < 0 or _end < _start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start or end index")

    query = db.query(Category.subject_class).filter(Category.archive == archive)

    if _order == "DESC":
        query = query.order_by(Category.subject_class.desc())
    else:
        query = query.order_by(Category.subject_class.asc())

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    return [{"id": cat.subject_class, "name": cat.subject_class, "description": cat.subject_class} for cat in query.offset(_start).limit(_end - _start).all()]


@router.get('/{archive}/subject-class/{subject_class}')
async def get_category(
        response: Response,
        archive: str,
        subject_class: str,
        db: Session = Depends(get_db)
    ) -> CategoryModel:
    query = db.query(Category).filter(Category.archive == archive, Category.subject_class == subject_class)
    count = query.count()
    if count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    response.headers['X-Total-Count'] = "1"
    return query.all()[0]


@router.get('/{id:int}')
async def get_category(id: int, db: Session = Depends(get_db)) -> CategoryModel:
    item = CategoryModel.base_select(db).filter(Category.request_id == id).all()
    if item:
        return CategoryModel.from_orm(item[0])
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id:int}')
async def update_category(
        request: Request,
        id: int,
        session: Session = Depends(transaction)) -> CategoryModel:
    body = await request.json()

    item = session.query(Category).filter(Category.request_id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify?
    for key, value in body.items():
        if key in item.__dict__:
            setattr(item, key, value)

    session.commit()
    session.refresh(item)  # Refresh the instance with the updated data
    return CategoryModel.from_orm(item)


@router.post('/')
async def create_category(
        request: Request,
        session: Session = Depends(transaction)) -> CategoryModel:
    body = await request.json()

    item = Category(**body)
    session.add(item)
    session.commit()
    session.refresh(item)
    return CategoryModel.from_orm(item)


@router.delete('/{id:int}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        id: int,
        session: Session = Depends(transaction)) -> Response:

    item = session.query(Category).filter(Category.request_id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")

    item.delete_instance()
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
