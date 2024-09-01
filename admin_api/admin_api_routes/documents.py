"""arXiv paper display routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from typing import Optional, List
from arxiv.base import logging
from arxiv.db.models import Document
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, date, timedelta
from .models import CrossControlModel
import re

from . import is_admin_user, get_db, datetime_to_epoch, VERY_OLDE

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(is_admin_user)], prefix="/documents")

class DocumentModel(BaseModel):
    id: int # document_id
    paper_id: str
    title: str
    authors: Optional[str]
    submitter_email: str
    submitter_id: Optional[int]
    dated: datetime
    primary_subject_class: Optional[str]
    created: Optional[datetime]

    class Config:
        orm_mode = True

    @staticmethod
    def base_select(db: Session):
        return db.query(
            Document.document_id.label("id"),
            Document.paper_id,
            Document.title,
            Document.authors,
            Document.submitter_email,
            Document.submitter_id,
            Document.dated,
            Document.primary_subject_class,
            Document.created)



@router.get('/')
async def list_documents(
        response: Response,
        _sort: Optional[str] = Query("id", description="sort by"),
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        id: Optional[List[int]] = Query(None, description="List of document IDs to filter by"),
        preset: Optional[str] = Query(None),
        start_date: Optional[date] = Query(None, description="Start date for filtering"),
        end_date: Optional[date] = Query(None, description="End date for filtering"),
        db: Session = Depends(get_db)
    ) -> List[DocumentModel]:
    query = DocumentModel.base_select(db)

    if _start < 0 or _end < _start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid start or end index")
    if id is None:
        t0 = datetime.now()

        order_columns = []
        if _sort:
            keys = _sort.split(",")
            for key in keys:
                if key == "id":
                    key = "document_id"
                try:
                    order_column = getattr(Document, key)
                    order_columns.append(order_column)
                except AttributeError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Invalid start or end index")

        if preset is not None:
            matched = re.search("last_(\d+)_days", preset)
            if matched:
                t_begin = datetime_to_epoch(None, t0 - timedelta(days=int(matched.group(1))))
                t_end = datetime_to_epoch(None, t0)
                query = query.filter(Document.dated.between(t_begin, t_end))
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid preset format")
        else:
            if start_date or end_date:
                t_begin = datetime_to_epoch(start_date, VERY_OLDE)
                t_end = datetime_to_epoch(end_date, date.today(), hour=23, minute=59, second=59)
                query = query.filter(Document.dated.between(t_begin, t_end))


        for column in order_columns:
            if _order == "DESC":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column.asc())
    else:
        query = query.filter(Document.document_id.in_(id))

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    result = [DocumentModel.from_orm(item) for item in query.offset(_start).limit(_end - _start).all()]
    return result


@router.get("/paper_id/{paper_id:str}")
def get_document(paper_id:str,
                 session: Session = Depends(get_db)) -> DocumentModel:
    """Display a paper."""
    query = DocumentModel.base_select(session).filter(Document.paper_id == paper_id)
    doc = query.all()
    if not doc:
        raise HTTPException(status_code=404, detail="Paper not found")
    return doc[0]

@router.get("/{id:str}")
def get_document(id:int,
                 session: Session = Depends(get_db)) -> DocumentModel:
    """Display a paper."""
    query = DocumentModel.base_select(session).filter(Document.document_id == id)
    doc = query.all()
    if not doc:
        raise HTTPException(status_code=404, detail="Paper not found")
    return doc[0]

