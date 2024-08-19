"""Provides integration for the external user interface."""
import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Response
from typing import Optional, List
from arxiv.base import logging
from arxiv.db.models import TapirEmailTemplate, TapirUser, TapirNickname
from arxiv.db import transaction
from sqlalchemy import select
from sqlalchemy.orm import Session, aliased
from pydantic import BaseModel

from . import is_admin_user, get_db

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(is_admin_user)], prefix="/email_templates")

class EmailTemplateModel(BaseModel):
    class Config:
        orm_mode = True
    id: int
    short_name: str
    long_name: str
    lang: str
    data: str
    sql_statement: str
    created_by: int
    updated_by: int
    updated_date: Optional[datetime.datetime]
    workflow_status: str
    flag_system: bool
    creator_first_name: str
    creator_last_name: str
    updater_first_name: str
    updater_last_name: str

    @staticmethod
    def base_select(db: Session):
        creator = aliased(TapirUser)
        updater = aliased(TapirUser)
        return db.query(
            TapirEmailTemplate.template_id.label("id"),
            TapirEmailTemplate.short_name.label("short_name"),
            TapirEmailTemplate.lang,
            TapirEmailTemplate.long_name.label("long_name"),
            TapirEmailTemplate.data,
            TapirEmailTemplate.sql_statement,

            creator.first_name.label("creator_first_name"),
            creator.last_name.label("creator_last_name"),
            updater.first_name.label("updater_first_name"),
            updater.last_name.label("updater_last_name"),
            TapirEmailTemplate.update_date,
            TapirEmailTemplate.created_by,
            TapirEmailTemplate.updated_by,
            TapirEmailTemplate.workflow_status,
            TapirEmailTemplate.flag_system,
        ).join(creator, TapirEmailTemplate.created_by == creator.user_id).join(updater, TapirEmailTemplate.updated_by == updater.user_id)

    pass

@router.get('/')
async def list_templates(
        response: Response,
        _sort: Optional[str] = Query("short_name", description="sort by"),
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        short_name: Optional[str] = Query(None),
        long_name: Optional[str] = Query(None),
        start_date: Optional[datetime.datetime] = Query(None, description="Start date for filtering"),
        end_date: Optional[datetime.datetime] = Query(None, description="End date for filtering"),
        db: Session = Depends(get_db)
    ) -> List[EmailTemplateModel]:
    query = EmailTemplateModel.base_select(db)

    if _start < 0 or _end < _start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start or end index")

    order_columns = []
    if _sort:
        keys = _sort.split(",")
        for key in keys:
            if key == "id":
                key = "template_id"
            try:
                order_column = getattr(TapirEmailTemplate, key)
                order_columns.append(order_column)
            except AttributeError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid start or end index")

    if short_name:
        query = query.filter(TapirEmailTemplate.short_name.contains(short_name))

    if long_name:
        query = query.filter(TapirEmailTemplate.long_name.contains(long_name))

    if start_date:
        query = query.filter(TapirEmailTemplate.update_date >= start_date)

    if end_date:
        query = query.filter(TapirEmailTemplate.update_date <= end_date)

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    result = [EmailTemplateModel.from_orm(item) for item in query.offset(_start).limit(_end - _start).all()]
    return result


@router.get('/{id:int}')
async def template_data(id: int, db: Session = Depends(get_db)) -> EmailTemplateModel:
    item = EmailTemplateModel.base_select(db).filter(TapirEmailTemplate.template_id == id).all()
    if item:
        return EmailTemplateModel.from_orm(item[0])
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id:int}')
async def update_template(request: Request,
                          id: int,
                          session: Session = Depends(transaction)) -> EmailTemplateModel:
    body = await request.json()

    item = session.query(TapirEmailTemplate).filter(TapirEmailTemplate.template_id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify?
    for key, value in body.items():
        if key in item.__dict__:
            setattr(item, key, value)

    session.commit()
    session.refresh(item)  # Refresh the instance with the updated data
    return EmailTemplateModel.from_orm(item)


@router.post('/')
async def create_email_template(request: Request, db: Session = Depends(transaction)) -> EmailTemplateModel:
    body = await request.json()

    item = TapirEmailTemplate(**body)
    db.add(item)
    db.commit()
    db.refresh(item)
    return EmailTemplateModel.from_orm(item)
