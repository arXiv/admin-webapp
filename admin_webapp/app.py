"""Provides application for development purposes."""
from .factory import create_web_app
import arxiv_db
# for table_name, table in arxiv_db.Base.metadata.tables.items():
#     print(f"Table: {table_name}")
#     print("-" * 50)
app = create_web_app()
# with app.app_context():
#     legacy.create_all()
