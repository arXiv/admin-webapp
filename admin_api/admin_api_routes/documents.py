"""arXiv paper display routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from arxiv.base import logging
from arxiv.db.models import Document
from adminapi_controllers.models import DocumentModel
from arxiv.db import get_db, transaction
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from . import is_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(is_admin_user)], prefix="/documents")

@router.get("/{paper_id:str}")
def get_document(paper_id:str,
                 _db: Session = Depends(get_db)) -> DocumentModel:
    """Display a paper."""
    return select(Document).filter(Document.paper_id == paper_id)
