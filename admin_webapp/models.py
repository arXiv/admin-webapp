
from sqlalchemy import Column, ForeignKey, text, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import TINYINT
from arxiv_db import Base

metadata = Base.metadata


class Moderators(Base):
    # __table__ = metadata.tables['arXiv_moderators']
    # __table_args__ = (
    #     PrimaryKeyConstraint(['user_id', 'archive','subject_class']),
    # )
        # __table_args__ = (
        # ForeignKeyConstraint(['policy_class'], ['tapir_policy_classes.class_id'], name='0_510'),
        # Index('email', 'email', unique=True),
    __tablename__ = 'arXiv_moderators'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True)
    archive = Column(ForeignKey('arXiv_categories.archive'), primary_key=True, nullable=False, server_default=text("''"))
    subject_class = Column(ForeignKey('arXiv_categories.subject_class'), primary_key=True, nullable=False, server_default=text("''"))

    is_public = Column(TINYINT(4), server_default=text("'0"))
    no_email = Column(TINYINT(1), server_default=text("'0"))
    no_web_email = Column(TINYINT(1), server_default=text("'0"))
    no_reply_to = Column(TINYINT(1), server_default=text("'0"))
    daily_update = Column(TINYINT(1), server_default=text("'0"))

# # TODO: set up relationship with Tapir Users?

# from sqlalchemy import BINARY, BigInteger, CHAR, Column, Date, DateTime, Enum, ForeignKeyConstraint, Index, Integer, JSON, SmallInteger, String, TIMESTAMP, Table, Text, text
# from sqlalchemy.dialects.mysql import CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
# from sqlalchemy.orm import relationship


# from .. import Base

# metadata = arxiv_db.Base.metadata

# from arxiv_db.models.sqa_types import EpochIntArxivTz
# # tapir_users



# class TapirUsers(arxiv_db.Base):
#     __tablename__ = 'tapir_users'
#     __table_args__ = (
#         ForeignKeyConstraint(['policy_class'], ['tapir_policy_classes.class_id'], name='0_510'),
#         Index('email', 'email', unique=True),
#         Index('first_name', 'first_name'),
#         Index('flag_approved', 'flag_approved'),
#         Index('flag_banned', 'flag_banned'),
#         Index('flag_can_lock', 'flag_can_lock'),
#         Index('flag_deleted', 'flag_deleted'),
#         Index('flag_edit_users', 'flag_edit_users'),
#         Index('flag_internal', 'flag_internal'),
#         Index('joined_date', 'joined_date'),
#         Index('joined_ip_num', 'joined_ip_num'),
#         Index('last_name', 'last_name'),
#         Index('policy_class', 'policy_class'),
#         Index('tracking_cookie', 'tracking_cookie')
#     )

#     user_id = Column(INTEGER, primary_key=True)
#     share_first_name = Column(INTEGER, nullable=False, server_default=text("'1'"))
#     share_last_name = Column(INTEGER, nullable=False, server_default=text("'1'"))
#     email = Column(String(255), nullable=False, server_default=text("''"))
#     share_email = Column(INTEGER, nullable=False, server_default=text("'8'"))
#     email_bouncing = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     policy_class = Column(SMALLINT, nullable=False, server_default=text("'0'"))
#     joined_date = Column(EpochIntArxivTz, nullable=False, server_default=text("'0'"))
#     joined_remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     flag_internal = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     flag_edit_users = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     flag_edit_system = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     flag_email_verified = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     flag_approved = Column(INTEGER, nullable=False, server_default=text("'1'"))
#     flag_deleted = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     flag_banned = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     flag_wants_email = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     flag_html_email = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
#     flag_allow_tex_produced = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     flag_can_lock = Column(INTEGER, nullable=False, server_default=text("'0'"))
#     first_name = Column(String(50))
#     last_name = Column(String(50))
#     suffix_name = Column(String(50))
#     joined_ip_num = Column(String(16))

#     tapir_policy_classes = relationship('TapirPolicyClasses', back_populates='tapir_users')
#     arXiv_control_holds = relationship('ControlHolds', foreign_keys='[ControlHolds.last_changed_by]', back_populates='tapir_users')
#     arXiv_control_holds_ = relationship('ControlHolds', foreign_keys='[ControlHolds.placed_by]', back_populates='tapir_users_')
#     arXiv_documents = relationship('Documents', back_populates='submitter')
#     arXiv_moderator_api_key = relationship('ModeratorApiKey', back_populates='user')
#     tapir_address = relationship('TapirAddress', back_populates='user')
#     tapir_email_change_tokens = relationship('TapirEmailChangeTokens', back_populates='user')
#     tapir_email_templates = relationship('TapirEmailTemplates', foreign_keys='[TapirEmailTemplates.created_by]', back_populates='tapir_users')
#     tapir_email_templates_ = relationship('TapirEmailTemplates', foreign_keys='[TapirEmailTemplates.updated_by]', back_populates='tapir_users_')
#     tapir_email_tokens = relationship('TapirEmailTokens', back_populates='user')
#     tapir_nicknames = relationship('TapirNicknames', back_populates='user', uselist=False)
#     tapir_phone = relationship('TapirPhone', back_populates='user')
#     tapir_recovery_tokens = relationship('TapirRecoveryTokens', back_populates='user')
#     tapir_sessions = relationship('TapirSessions', back_populates='user')
#     arXiv_cross_control = relationship('CrossControl', back_populates='user')
#     arXiv_endorsement_requests = relationship('EndorsementRequests', back_populates='endorsee')
#     arXiv_jref_control = relationship('JrefControl', back_populates='user')
#     arXiv_metadata = relationship('Metadata', back_populates='submitter')
#     arXiv_show_email_requests = relationship('ShowEmailRequests', back_populates='user')
#     arXiv_submission_control = relationship('SubmissionControl', back_populates='user')
#     arXiv_submissions = relationship('Submissions', back_populates='submitter')
#     tapir_admin_audit = relationship('TapirAdminAudit', foreign_keys='[TapirAdminAudit.admin_user]', back_populates='tapir_users')
#     tapir_admin_audit_ = relationship('TapirAdminAudit', foreign_keys='[TapirAdminAudit.affected_user]', back_populates='tapir_users_')
#     tapir_email_mailings = relationship('TapirEmailMailings', foreign_keys='[TapirEmailMailings.created_by]', back_populates='tapir_users')
#     tapir_email_mailings_ = relationship('TapirEmailMailings', foreign_keys='[TapirEmailMailings.sent_by]', back_populates='tapir_users_')
#     tapir_permanent_tokens = relationship('TapirPermanentTokens', back_populates='user')
#     tapir_recovery_tokens_used = relationship('TapirRecoveryTokensUsed', back_populates='user')

#     endorsee_of = relationship('Endorsements', foreign_keys='[Endorsements.endorsee_id]', back_populates='endorsee')
#     endorses = relationship('Endorsements', foreign_keys='[Endorsements.endorser_id]', back_populates='endorser')

#     arXiv_ownership_requests = relationship('OwnershipRequests', back_populates='user')
#     arXiv_submission_category_proposal = relationship('SubmissionCategoryProposal', back_populates='user')
#     arXiv_submission_flag = relationship('SubmissionFlag', back_populates='user')
#     arXiv_submission_hold_reason = relationship('SubmissionHoldReason', back_populates='user')
#     arXiv_submission_view_flag = relationship('SubmissionViewFlag', back_populates='user')

#     owned_papers = relationship("PaperOwners",  foreign_keys="[PaperOwners.user_id]", back_populates="owner")

#     demographics = relationship('Demographics', foreign_keys="[Demographics.user_id]", uselist=False)

#     @property
#     def display_name(self):
#         return f"{self.first_name} {self.last_name}"

#     @property
#     def nickname(self):
#         """Gets user's nickname.

#         This will query out to the DB if the tapir_nicknames isn't already loaded.
#         Do that with `.options(loadjoin(TapirUsers.tapir_nicknames))`.
#         """
#         try:
#             return self.tapir_nicknames.nickname
#         except ValueError:
#             return f"no-nick-{self.user_id}"

