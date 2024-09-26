"""arXiv submission routes."""
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Response

from sqlalchemy import select, update, func, case, Select, distinct, exists, and_
from sqlalchemy.orm import Session, joinedload

from pydantic import BaseModel
from arxiv.base import logging
from arxiv.db import transaction
from arxiv.db.models import Submission, Demographic, TapirUser, Category, SubmissionCategory

from . import get_db, is_any_user, get_current_user
from .categories import CategoryModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/submission_categories", dependencies=[Depends(is_any_user)])


class SubmissionCategoryModel(BaseModel):
    class Config:
        orm_mode = True

    id: int
    category: str
    is_primary: bool
    is_published: Optional[bool]

    @staticmethod
    def base_select(db: Session):
        return db.query(
            SubmissionCategory.submission_id.label("id"),
            SubmissionCategory.category,
            SubmissionCategory.is_primary,
            SubmissionCategory.is_published
        )
    pass


@router.get('/{id:int}/category/')
async def get_submission_categories(id: int,
                                  db: Session = Depends(get_db)) -> List[SubmissionCategoryModel]:
    cats = SubmissionCategoryModel.base_select(db).filter(SubmissionCategory.submission_id == id).all()
    return [SubmissionCategoryModel.from_orm(item) for item in cats]

@router.get('/{id:int}/category/{category:str}')
async def get_submission_category(id: int,
                                  category: str,
                                  db: Session = Depends(get_db)) -> SubmissionCategoryModel:
    item = SubmissionCategoryModel.base_select(db).filter(SubmissionCategory.submission_id == id).filter(SubmissionCategory.category == category).one_or_none()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return SubmissionCategoryModel.from_orm(item)