"""arXiv paper display routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from typing import Optional, List
from arxiv.base import logging
from arxiv.db.models import TapirSession, TapirSession
from sqlalchemy.orm import Session
from .models import CrossControlModel, TapirSessionModel

from . import is_admin_user, get_db, datetime_to_epoch, VERY_OLDE

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(is_admin_user)], prefix="/tapir_sessions")

def TapirSessionModel_base_select(db: Session):
    return db.query(TapirSession)

@router.get('/')
async def list_tapir_sessions(
        response: Response,
        _sort: Optional[str] = Query("id", description="sort by"),
        _order: Optional[str] = Query("ASC", description="sort order"),
        _start: Optional[int] = Query(0, alias="_start"),
        _end: Optional[int] = Query(100, alias="_end"),
        user_id: Optional[int] = Query(None, alias="User id"),
        id: Optional[List[int]] = Query(None, description="List of user IDs to filter by"),
        db: Session = Depends(get_db)
    ) -> List[TapirSessionModel]:
    query = TapirSessionModel_base_select(db)

    if id is not None:
        query = query.filter(TapirSession.user_id.in_(id))
    else:
        if _start < 0 or _end < _start:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid start or end index")
        if user_id:
            query = query.filter(TapirSession.user_id == user_id)

    order_columns = []
    if _sort:
        keys = _sort.split(",")
        for key in keys:
            if key == "id":
                key = "session_id"
            try:
                order_column = getattr(TapirSession, key)
                order_columns.append(order_column)
            except AttributeError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid start or end index")
    for column in order_columns:
        if _order == "DESC":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    count = query.count()
    response.headers['X-Total-Count'] = str(count)
    result = [TapirSessionModel.from_orm(item) for item in query.offset(_start).limit(_end - _start).all()]
    return result


@router.get("/{id:int}")
def get_tapir_session(
        id:int, session: Session = Depends(get_db)) -> TapirSessionModel:
    """Display a paper."""
    tapir_session = TapirSessionModel_base_select(session).filter(TapirSession.session_id == id).one_or_none()
    if not tapir_session:
        raise HTTPException(status_code=404, detail=f"TapirSession not found for {id}")
    return tapir_session


@router.get("/user/{id:int}")
def get_tapir_session_for_user(
        response: Response,
        id:int, session: Session = Depends(get_db)) -> List[TapirSessionModel]:
    """Display a paper."""
    tapir_session = TapirSessionModel_base_select(session).filter(TapirSession.session_id == id).all()
    count = tapir_session.count()
    response.headers['X-Total-Count'] = str(count)
    return tapir_session

