
from sqlalchemy import Column, ForeignKey, text, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import TINYINT
from arxiv_db import Base

metadata = Base.metadata


class Moderators(Base):
    __tablename__ = 'arXiv_moderators'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True)
    archive = Column(ForeignKey('arXiv_categories.archive'), primary_key=True, nullable=False, server_default=text("''"))
    subject_class = Column(ForeignKey('arXiv_categories.subject_class'), primary_key=True, nullable=False, server_default=text("''"))

    is_public = Column(TINYINT(4), server_default=text("'0"))
    no_email = Column(TINYINT(1), server_default=text("'0"))
    no_web_email = Column(TINYINT(1), server_default=text("'0"))
    no_reply_to = Column(TINYINT(1), server_default=text("'0"))
    daily_update = Column(TINYINT(1), server_default=text("'0"))

# TODO: set up relationship with Tapir Users?

