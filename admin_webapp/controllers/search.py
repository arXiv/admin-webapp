from flask import current_app, Response
from admin_webapp.extensions import get_db
from sqlalchemy import select
from arxiv_db.models import TapirUsers

"""
Searches based on
"""
def userid_search(search_string: str) -> Response:
    session = get_db(current_app).session
    
    stmt = (select(TapirUsers))
    