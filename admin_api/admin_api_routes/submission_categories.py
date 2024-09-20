"""arXiv submission routes."""
import re
from datetime import timedelta, datetime, date
from typing import Optional, List

from arxiv.auth.user_claims import ArxivUserClaims
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request, Response

from sqlalchemy import select, update, func, case, Select, distinct, exists, and_
from sqlalchemy.orm import Session, joinedload

from pydantic import BaseModel
from arxiv.base import logging
from arxiv.db import transaction
from arxiv.db.models import Submission, Demographic, TapirUser, Category, \
    SubmissionCategory

from . import is_admin_user, get_db, datetime_to_epoch, VERY_OLDE, is_any_user, get_current_user
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
        ).outerjoin(
            Demographic,
            Demographic.user_id == SubmissionCategory.endorsee_id,
        )
    pass


@router.get('/{id:int}/category/{category:str}')
async def get_submission_category(id: int,
                                  current_user: ArxivUserClaims = Depends(get_current_user),
                                  db: Session = Depends(get_db)) -> [SubmissionCategoryModel]:
    item: SubmissionCategory = SubmissionCategoryModel.base_select(db).filter(SubmissionCategory.submission_id == id).all()
