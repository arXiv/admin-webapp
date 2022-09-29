# coding: utf-8
# from typing import Optional, List
# from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
# from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import types as types

# from modapi.db import Base

# from arxiv import taxonomy as taxonomy

# metadata = Base.metadata

# # inverse of CATEGORY_ALIASES
# CATEGORY_ALIASES_INV={v: k for k, v in taxonomy.CATEGORY_ALIASES.items()}

# class SubscriptionUniversalInstitution(Base):
#     __tablename__ = 'Subscription_UniversalInstitution'

#     resolver_URL = Column(String(255))
#     name = Column(String(255), nullable=False, index=True)
#     label = Column(String(255))
#     id = Column(INTEGER(11), primary_key=True)
#     alt_text = Column(String(255))
#     link_icon = Column(String(255))
#     note = Column(String(255))


# class AdminLog(Base):
#     __tablename__ = 'arXiv_admin_log'

#     id = Column(INTEGER(11), primary_key=True)
#     logtime = Column(String(24))
#     created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#     paper_id = Column(String(20), index=True)
#     username = Column(String(20), index=True)
#     host = Column(String(64))
#     program = Column(String(20))
#     command = Column(String(20), index=True)
#     logtext = Column(Text)
#     document_id = Column(MEDIUMINT(8))
#     submission_id = Column(INTEGER(11), index=True)
#     notify = Column(TINYINT(1), server_default=text("'0'"))


# t_arXiv_admin_state = Table(
#     'arXiv_admin_state', metadata,
#     Column('document_id', INTEGER(11), unique=True),
#     Column('timestamp', TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
#     Column('abs_timestamp', INTEGER(11)),
#     Column('src_timestamp', INTEGER(11)),
#     Column('state', Enum('pending', 'ok', 'bad'), nullable=False, server_default=text("'pending'")),
#     Column('admin', String(32)),
#     Column('comment', String(255))
# )


# class ArchiveCategory(Base):
#     __tablename__ = 'arXiv_archive_category'

#     archive_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
#     category_id = Column(String(32), primary_key=True, nullable=False)


# class ArchiveDef(Base):
#     __tablename__ = 'arXiv_archive_def'

#     archive = Column(String(16), primary_key=True, server_default=text("''"))
#     name = Column(String(255))


# class ArchiveGroup(Base):
#     __tablename__ = 'arXiv_archive_group'

#     archive_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
#     group_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))


# class AwsConfig(Base):
#     __tablename__ = 'arXiv_aws_config'

#     domain = Column(String(75), primary_key=True, nullable=False)
#     keyname = Column(String(60), primary_key=True, nullable=False)
#     value = Column(String(150))


# class AwsFiles(Base):
#     __tablename__ = 'arXiv_aws_files'

#     type = Column(String(10), nullable=False, index=True, server_default=text("''"))
#     filename = Column(String(100), primary_key=True, server_default=text("''"))
#     md5sum = Column(String(50))
#     content_md5sum = Column(String(50))
#     size = Column(INTEGER(11))
#     timestamp = Column(DateTime)
#     yymm = Column(String(4))
#     seq_num = Column(INTEGER(11))
#     first_item = Column(String(20))
#     last_item = Column(String(20))
#     num_items = Column(INTEGER(11))


# class BibFeeds(Base):
#     __tablename__ = 'arXiv_bib_feeds'

#     bib_id = Column(MEDIUMINT(8), primary_key=True)
#     name = Column(String(64), nullable=False, server_default=text("''"))
#     priority = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     uri = Column(String(255))
#     identifier = Column(String(255))
#     version = Column(String(255))
#     strip_journal_ref = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     concatenate_dupes = Column(INTEGER(11))
#     max_updates = Column(INTEGER(11))
#     email_errors = Column(String(255))
#     prune_ids = Column(Text)
#     prune_regex = Column(Text)
#     enabled = Column(TINYINT(1), server_default=text("'0'"))


# class BibUpdates(Base):
#     __tablename__ = 'arXiv_bib_updates'

#     update_id = Column(MEDIUMINT(8), primary_key=True)
#     document_id = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
#     bib_id = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
#     updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
#     journal_ref = Column(Text)
#     doi = Column(Text)


# t_arXiv_black_email = Table(
#     'arXiv_black_email', metadata,
#     Column('pattern', String(64))
# )


# t_arXiv_block_email = Table(
#     'arXiv_block_email', metadata,
#     Column('pattern', String(64))
# )


# class BogusCountries(Base):
#     __tablename__ = 'arXiv_bogus_countries'

#     user_id = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
#     country_name = Column(String(255), nullable=False, server_default=text("''"))


# class DblpAuthors(Base):
#     __tablename__ = 'arXiv_dblp_authors'

#     author_id = Column(MEDIUMINT(8), primary_key=True, unique=True)
#     name = Column(String(40), unique=True)


# class EndorsementDomains(Base):
#     __tablename__ = 'arXiv_endorsement_domains'

#     endorsement_domain = Column(String(32), primary_key=True, server_default=text("''"))
#     endorse_all = Column(Enum('y', 'n'), nullable=False, server_default=text("'n'"))
#     mods_endorse_all = Column(Enum('y', 'n'), nullable=False, server_default=text("'n'"))
#     endorse_email = Column(Enum('y', 'n'), nullable=False, server_default=text("'y'"))
#     papers_to_endorse = Column(SMALLINT(5), nullable=False, server_default=text("'4'"))


# class FreezeLog(Base):
#     __tablename__ = 'arXiv_freeze_log'

#     date = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))


# class GroupDef(Base):
#     __tablename__ = 'arXiv_group_def'

#     archive_group = Column(String(16), primary_key=True, server_default=text("''"))
#     name = Column(String(255))


# class Groups(Base):
#     __tablename__ = 'arXiv_groups'

#     group_id = Column(String(16), primary_key=True, server_default=text("''"))
#     group_name = Column(String(255), nullable=False, server_default=text("''"))
#     start_year = Column(String(4), nullable=False, server_default=text("''"))


# class Licenses(Base):
#     __tablename__ = 'arXiv_licenses'

#     name = Column(String(255), primary_key=True)
#     label = Column(String(255))
#     active = Column(TINYINT(1), server_default=text("'1'"))
#     note = Column(String(255))
#     sequence = Column(TINYINT(4))


# class LogPositions(Base):
#     __tablename__ = 'arXiv_log_positions'

#     id = Column(String(255), primary_key=True, server_default=text("''"))
#     position = Column(INTEGER(10))
#     date = Column(INTEGER(10))


# class MonitorKlog(Base):
#     __tablename__ = 'arXiv_monitor_klog'

#     t = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
#     sent = Column(INTEGER(10))


# class MonitorMailq(Base):
#     __tablename__ = 'arXiv_monitor_mailq'

#     t = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
#     main_q = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     local_q = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     local_host_map = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     local_timeout = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     local_refused = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     local_in_flight = Column(INTEGER(10), nullable=False, server_default=text("'0'"))


# class MonitorMailsent(Base):
#     __tablename__ = 'arXiv_monitor_mailsent'

#     t = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
#     sent = Column(INTEGER(10))


# class NextMail(Base):
#     __tablename__ = 'arXiv_next_mail'
#     __table_args__ = (
#         Index('arXiv_next_mail_idx_document_id_version', 'document_id', 'version'),
#     )

#     next_mail_id = Column(INTEGER(11), primary_key=True)
#     submission_id = Column(INTEGER(11), nullable=False)
#     document_id = Column(MEDIUMINT(8), nullable=False, index=True, server_default=text("'0'"))
#     paper_id = Column(String(20))
#     version = Column(INTEGER(4), nullable=False, server_default=text("'1'"))
#     type = Column(String(255), nullable=False, server_default=text("'new'"))
#     extra = Column(String(255))
#     mail_id = Column(CHAR(6))
#     is_written = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


# class OrcidConfig(Base):
#     __tablename__ = 'arXiv_orcid_config'

#     domain = Column(String(75), primary_key=True, nullable=False)
#     keyname = Column(String(60), primary_key=True, nullable=False)
#     value = Column(String(150))


# t_arXiv_ownership_requests_papers = Table(
#     'arXiv_ownership_requests_papers', metadata,
#     Column('request_id', INTEGER(10), nullable=False, server_default=text("'0'")),
#     Column('document_id', INTEGER(10), nullable=False, index=True, server_default=text("'0'")),
#     Index('request_id', 'request_id', 'document_id', unique=True)
# )


# class PaperSessions(Base):
#     __tablename__ = 'arXiv_paper_sessions'

#     paper_session_id = Column(INTEGER(10), primary_key=True)
#     paper_id = Column(String(16), nullable=False, server_default=text("''"))
#     start_time = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     end_time = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     ip_name = Column(String(16), nullable=False, server_default=text("''"))


# class PublishLog(Base):
#     __tablename__ = 'arXiv_publish_log'

#     date = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))


# t_arXiv_refresh_list = Table(
#     'arXiv_refresh_list', metadata,
#     Column('filename', String(255)),
#     Column('mtime', INTEGER(10), index=True)
# )


# class RejectSessionUsernames(Base):
#     __tablename__ = 'arXiv_reject_session_usernames'

#     username = Column(String(64), primary_key=True, server_default=text("''"))


# class SciencewisePings(Base):
#     __tablename__ = 'arXiv_sciencewise_pings'

#     paper_id_v = Column(String(32), primary_key=True)
#     updated = Column(DateTime)


# class State(Base):
#     __tablename__ = 'arXiv_state'

#     id = Column(INTEGER(11), primary_key=True)
#     name = Column(String(24))
#     value = Column(String(24))


# t_arXiv_stats_hourly = Table(
#     'arXiv_stats_hourly', metadata,
#     Column('ymd', Date, nullable=False, index=True),
#     Column('hour', TINYINT(3), nullable=False, index=True),
#     Column('node_num', TINYINT(3), nullable=False, index=True),
#     Column('access_type', CHAR(1), nullable=False, index=True),
#     Column('connections', INTEGER(4), nullable=False)
# )


# class StatsMonthlyDownloads(Base):
#     __tablename__ = 'arXiv_stats_monthly_downloads'

#     ym = Column(Date, primary_key=True)
#     downloads = Column(INTEGER(10), nullable=False)


# class StatsMonthlySubmissions(Base):
#     __tablename__ = 'arXiv_stats_monthly_submissions'

#     ym = Column(Date, primary_key=True, server_default=text("'0000-00-00'"))
#     num_submissions = Column(SMALLINT(5), nullable=False)
#     historical_delta = Column(TINYINT(4), nullable=False, server_default=text("'0'"))


# class SubmitterFlags(Base):
#     __tablename__ = 'arXiv_submitter_flags'

#     flag_id = Column(INTEGER(11), primary_key=True)
#     comment = Column(String(255))
#     pattern = Column(String(255))


# class SuspectEmails(Base):
#     __tablename__ = 'arXiv_suspect_emails'

#     id = Column(INTEGER(11), primary_key=True)
#     type = Column(String(10), nullable=False)
#     pattern = Column(Text, nullable=False)
#     comment = Column(Text, nullable=False)
#     updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


# class Titles(Base):
#     __tablename__ = 'arXiv_titles'

#     paper_id = Column(String(64), primary_key=True)
#     title = Column(String(255), index=True)
#     report_num = Column(String(255), index=True)
#     date = Column(Date)


# class TrackbackPings(Base):
#     __tablename__ = 'arXiv_trackback_pings'

#     trackback_id = Column(MEDIUMINT(8), primary_key=True)
#     document_id = Column(MEDIUMINT(8), index=True)
#     title = Column(String(255), nullable=False, server_default=text("''"))
#     excerpt = Column(String(255), nullable=False, server_default=text("''"))
#     url = Column(String(255), nullable=False, index=True, server_default=text("''"))
#     blog_name = Column(String(255), nullable=False, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     remote_addr = Column(String(16), nullable=False, server_default=text("''"))
#     posted_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     is_stale = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
#     approved_by_user = Column(MEDIUMINT(9), nullable=False, server_default=text("'0'"))
#     approved_time = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
#     status = Column(Enum('pending', 'pending2', 'accepted', 'rejected', 'spam'), nullable=False, index=True, server_default=text("'pending'"))
#     site_id = Column(INTEGER(10))


# class TrackbackSites(Base):
#     __tablename__ = 'arXiv_trackback_sites'

#     pattern = Column(String(255), nullable=False, index=True, server_default=text("''"))
#     site_id = Column(INTEGER(10), primary_key=True)
#     action = Column(Enum('neutral', 'accept', 'reject', 'spam'), nullable=False, server_default=text("'neutral'"))


# class Tracking(Base):
#     __tablename__ = 'arXiv_tracking'

#     tracking_id = Column(INTEGER(11), primary_key=True)
#     sword_id = Column(INTEGER(8), nullable=False, unique=True, server_default=text("'00000000'"))
#     paper_id = Column(String(32), nullable=False)
#     submission_errors = Column(Text)
#     timestamp = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


# t_arXiv_updates = Table(
#     'arXiv_updates', metadata,
#     Column('document_id', INTEGER(11), index=True),
#     Column('version', INTEGER(4), nullable=False, server_default=text("'1'")),
#     Column('date', Date, index=True),
#     Column('action', Enum('new', 'replace', 'absonly', 'cross', 'repcro')),
#     Column('archive', String(20), index=True),
#     Column('category', String(20), index=True),
#     Index('document_id', 'document_id', 'date', 'action', 'category', unique=True)
# )


# t_arXiv_updates_tmp = Table(
#     'arXiv_updates_tmp', metadata,
#     Column('document_id', INTEGER(11)),
#     Column('date', Date),
#     Column('action', Enum('new', 'replace', 'absonly', 'cross', 'repcro')),
#     Column('category', String(20)),
#     Index('document_id', 'document_id', 'date', 'action', 'category', unique=True)
# )


# t_arXiv_white_email = Table(
#     'arXiv_white_email', metadata,
#     Column('pattern', String(64))
# )


# t_arXiv_xml_notifications = Table(
#     'arXiv_xml_notifications', metadata,
#     Column('control_id', INTEGER(10), index=True),
#     Column('type', Enum('submission', 'cross', 'jref')),
#     Column('queued_date', INTEGER(10), nullable=False, server_default=text("'0'")),
#     Column('sent_date', INTEGER(10), nullable=False, server_default=text("'0'")),
#     Column('status', Enum('unsent', 'sent', 'failed'), index=True)
# )


# class DbixClassSchemaVersions(Base):
#     __tablename__ = 'dbix_class_schema_versions'

#     version = Column(String(10), primary_key=True)
#     installed = Column(String(20), nullable=False)


# t_demographics_backup = Table(
#     'demographics_backup', metadata,
#     Column('user_id', INTEGER(10), nullable=False, server_default=text("'0'")),
#     Column('country', CHAR(2), nullable=False, server_default=text("''")),
#     Column('affiliation', String(255), nullable=False, server_default=text("''")),
#     Column('url', String(255), nullable=False, server_default=text("''")),
#     Column('type', SMALLINT(5)),
#     Column('os', SMALLINT(5)),
#     Column('archive', String(16)),
#     Column('subject_class', String(16)),
#     Column('original_subject_classes', String(255), nullable=False, server_default=text("''")),
#     Column('flag_group_physics', INTEGER(1)),
#     Column('flag_group_math', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_group_cs', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_group_nlin', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_proxy', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_journal', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_xml', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('dirty', INTEGER(1), nullable=False, server_default=text("'2'")),
#     Column('flag_group_test', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_suspect', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_group_q_bio', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_no_upload', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_no_endorse', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('veto_status', Enum('ok', 'no-endorse', 'no-upload'), server_default=text("'ok'"))
# )


# class Sessions(Base):
#     __tablename__ = 'sessions'

#     id = Column(CHAR(72), primary_key=True)
#     session_data = Column(Text)
#     expires = Column(INTEGER(11))


# class TapirCountries(Base):
#     __tablename__ = 'tapir_countries'

#     digraph = Column(CHAR(2), primary_key=True, server_default=text("''"))
#     country_name = Column(String(255), nullable=False, server_default=text("''"))
#     rank = Column(INTEGER(1), nullable=False, server_default=text("'255'"))


# class TapirEmailLog(Base):
#     __tablename__ = 'tapir_email_log'

#     mail_id = Column(INTEGER(10), primary_key=True)
#     reference_type = Column(CHAR(1))
#     reference_id = Column(INTEGER(4))
#     sent_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     email = Column(String(50), nullable=False, server_default=text("''"))
#     flag_bounced = Column(INTEGER(1))
#     mailing_id = Column(INTEGER(10), index=True)
#     template_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))


# t_tapir_error_log = Table(
#     'tapir_error_log', metadata,
#     Column('error_date', INTEGER(4), nullable=False, index=True, server_default=text("'0'")),
#     Column('user_id', INTEGER(4), index=True),
#     Column('session_id', INTEGER(4), index=True),
#     Column('ip_addr', String(16), nullable=False, index=True, server_default=text("''")),
#     Column('remote_host', String(255), nullable=False, server_default=text("''")),
#     Column('tracking_cookie', String(32), nullable=False, index=True, server_default=text("''")),
#     Column('message', String(32), nullable=False, index=True, server_default=text("''")),
#     Column('url', String(255), nullable=False, server_default=text("''")),
#     Column('error_url', String(255), nullable=False, server_default=text("''"))
# )


# class TapirIntegerVariables(Base):
#     __tablename__ = 'tapir_integer_variables'

#     variable_id = Column(String(32), primary_key=True, server_default=text("''"))
#     value = Column(INTEGER(4), nullable=False, server_default=text("'0'"))


# class TapirNicknamesAudit(Base):
#     __tablename__ = 'tapir_nicknames_audit'

#     nick_id = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
#     creation_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     creation_ip_num = Column(String(16), nullable=False, index=True, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     tracking_cookie = Column(String(255), nullable=False, index=True, server_default=text("''"))


# t_tapir_no_cookies = Table(
#     'tapir_no_cookies', metadata,
#     Column('log_date', INTEGER(10), nullable=False, server_default=text("'0'")),
#     Column('ip_addr', String(16), nullable=False, server_default=text("''")),
#     Column('remote_host', String(255), nullable=False, server_default=text("''")),
#     Column('tracking_cookie', String(255), nullable=False, server_default=text("''")),
#     Column('session_data', String(255), nullable=False, server_default=text("''")),
#     Column('user_agent', String(255), nullable=False, server_default=text("''"))
# )


# t_tapir_periodic_tasks_log = Table(
#     'tapir_periodic_tasks_log', metadata,
#     Column('t', INTEGER(4), nullable=False, index=True, server_default=text("'0'")),
#     Column('entry', Text)
# )


# class TapirPolicyClasses(Base):
#     __tablename__ = 'tapir_policy_classes'

#     class_id = Column(SMALLINT(5), primary_key=True)
#     name = Column(String(64), nullable=False, server_default=text("''"))
#     description = Column(Text, nullable=False)
#     password_storage = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     recovery_policy = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     permanent_login = Column(INTEGER(1), nullable=False, server_default=text("'0'"))


# class TapirPresessions(Base):
#     __tablename__ = 'tapir_presessions'

#     presession_id = Column(INTEGER(4), primary_key=True)
#     ip_num = Column(String(16), nullable=False, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
#     created_at = Column(INTEGER(4), nullable=False, server_default=text("'0'"))


# class TapirStringVariables(Base):
#     __tablename__ = 'tapir_string_variables'

#     variable_id = Column(String(32), primary_key=True, server_default=text("''"))
#     value = Column(Text, nullable=False)


# class TapirStrings(Base):
#     __tablename__ = 'tapir_strings'

#     name = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
#     module = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
#     language = Column(String(32), primary_key=True, nullable=False, server_default=text("'en'"))
#     string = Column(Text, nullable=False)


# class SubscriptionUniversalInstitutionContact(Base):
#     __tablename__ = 'Subscription_UniversalInstitutionContact'

#     email = Column(String(255))
#     sid = Column(ForeignKey('Subscription_UniversalInstitution.id', ondelete='CASCADE'), nullable=False, index=True)
#     active = Column(TINYINT(4), server_default=text("'0'"))
#     contact_name = Column(String(255))
#     id = Column(INTEGER(11), primary_key=True)
#     phone = Column(String(255))
#     note = Column(String(2048))

#     Subscription_UniversalInstitution = relationship('SubscriptionUniversalInstitution')


# class SubscriptionUniversalInstitutionIP(Base):
#     __tablename__ = 'Subscription_UniversalInstitutionIP'
#     __table_args__ = (
#         Index('ip', 'start', 'end'),
#     )

#     sid = Column(ForeignKey('Subscription_UniversalInstitution.id', ondelete='CASCADE'), nullable=False, index=True)
#     id = Column(INTEGER(11), primary_key=True)
#     exclude = Column(TINYINT(4), server_default=text("'0'"))
#     end = Column(BIGINT(20), nullable=False, index=True)
#     start = Column(BIGINT(20), nullable=False, index=True)

#     Subscription_UniversalInstitution = relationship('SubscriptionUniversalInstitution')


# class Archives(Base):
#     __tablename__ = 'arXiv_archives'

#     archive_id = Column(String(16), primary_key=True, server_default=text("''"))
#     in_group = Column(ForeignKey('arXiv_groups.group_id'), nullable=False, index=True, server_default=text("''"))
#     archive_name = Column(String(255), nullable=False, server_default=text("''"))
#     start_date = Column(String(4), nullable=False, server_default=text("''"))
#     end_date = Column(String(4), nullable=False, server_default=text("''"))
#     subdivided = Column(INTEGER(1), nullable=False, server_default=text("'0'"))

#     arXiv_groups = relationship('Groups')


# t_tapir_save_post_variables = Table(
#     'tapir_save_post_variables', metadata,
#     Column('presession_id', ForeignKey('tapir_presessions.presession_id'), nullable=False, index=True, server_default=text("'0'")),
#     Column('name', String(255)),
#     Column('value', MEDIUMTEXT, nullable=False),
#     Column('seq', INTEGER(4), nullable=False, server_default=text("'0'"))
# )


# class TapirUsers(Base):
#     __tablename__ = 'tapir_users'

#     user_id = Column(INTEGER(4), primary_key=True)
#     first_name = Column(String(50), index=True)
#     last_name = Column(String(50), index=True)
#     suffix_name = Column(String(50))
#     share_first_name = Column(INTEGER(1), nullable=False, server_default=text("'1'"))
#     share_last_name = Column(INTEGER(1), nullable=False, server_default=text("'1'"))
#     email = Column(String(255), nullable=False, unique=True, server_default=text("''"))
#     share_email = Column(INTEGER(1), nullable=False, server_default=text("'8'"))
#     email_bouncing = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     policy_class = Column(ForeignKey('tapir_policy_classes.class_id'), nullable=False, index=True, server_default=text("'0'"))
#     joined_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     joined_ip_num = Column(String(16), index=True)
#     joined_remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     flag_internal = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_edit_users = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_edit_system = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     flag_email_verified = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     flag_approved = Column(INTEGER(1), nullable=False, index=True, server_default=text("'1'"))
#     flag_deleted = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_banned = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_wants_email = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     flag_html_email = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     tracking_cookie = Column(String(255), nullable=False, index=True, server_default=text("''"))
#     flag_allow_tex_produced = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     flag_can_lock = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))

#     tapir_policy_classes = relationship('TapirPolicyClasses')
#     username = relationship("TapirNicknames", uselist=False, viewonly=True)
#     demographics = relationship("Demographics", uselist=False)


# class AuthorIds(Base):
#     __tablename__ = 'arXiv_author_ids'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True)
#     author_id = Column(String(50), nullable=False, index=True)
#     updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

#     user = relationship('TapirUsers', uselist=False)


# t_arXiv_bad_pw = Table(
#     'arXiv_bad_pw', metadata,
#     Column('user_id', ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
# )


# class Categories(Base):
#     __tablename__ = 'arXiv_categories'

#     archive = Column(ForeignKey('arXiv_archives.archive_id'), primary_key=True, nullable=False, server_default=text("''"))
#     subject_class = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
#     definitive = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     active = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     category_name = Column(String(255))
#     endorse_all = Column(Enum('y', 'n', 'd'), nullable=False, server_default=text("'d'"))
#     endorse_email = Column(Enum('y', 'n', 'd'), nullable=False, server_default=text("'d'"))
#     papers_to_endorse = Column(SMALLINT(5), nullable=False, server_default=text("'0'"))
#     endorsement_domain = Column(ForeignKey('arXiv_endorsement_domains.endorsement_domain'), index=True)

#     arXiv_archives = relationship('Archives')
#     arXiv_endorsement_domains = relationship('EndorsementDomains')


# class ControlHolds(Base):
#     __tablename__ = 'arXiv_control_holds'
#     __table_args__ = (
#         Index('control_id', 'control_id', 'hold_type', unique=True),
#     )

#     hold_id = Column(INTEGER(10), primary_key=True)
#     control_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     hold_type = Column(Enum('submission', 'cross', 'jref'), nullable=False, index=True, server_default=text("'submission'"))
#     hold_status = Column(Enum('held', 'extended', 'accepted', 'rejected'), nullable=False, index=True, server_default=text("'held'"))
#     hold_reason = Column(String(255), nullable=False, index=True, server_default=text("''"))
#     hold_data = Column(String(255), nullable=False, server_default=text("''"))
#     origin = Column(Enum('auto', 'user', 'admin', 'moderator'), nullable=False, index=True, server_default=text("'auto'"))
#     placed_by = Column(ForeignKey('tapir_users.user_id'), index=True)
#     last_changed_by = Column(ForeignKey('tapir_users.user_id'), index=True)

#     tapir_users = relationship('TapirUsers', primaryjoin='ControlHolds.last_changed_by == TapirUsers.user_id')
#     tapir_users1 = relationship('TapirUsers', primaryjoin='ControlHolds.placed_by == TapirUsers.user_id')


# class Documents(Base):
#     __tablename__ = 'arXiv_documents'

#     document_id = Column(MEDIUMINT(8), primary_key=True)
#     paper_id = Column(String(20), nullable=False, unique=True, server_default=text("''"))
#     title = Column(String(255), nullable=False, index=True, server_default=text("''"))
#     authors = Column(Text)
#     submitter_email = Column(String(64), nullable=False, index=True, server_default=text("''"))
#     submitter_id = Column(ForeignKey('tapir_users.user_id'), index=True)
#     dated = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     primary_subject_class = Column(String(16))
#     created = Column(DateTime)

#     submitter = relationship('TapirUsers')


# t_arXiv_duplicates = Table(
#     'arXiv_duplicates', metadata,
#     Column('user_id', ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'")),
#     Column('email', String(255)),
#     Column('username', String(255))
# )


# class ModeratorApiKey(Base):
#     __tablename__ = 'arXiv_moderator_api_key'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
#     valid = Column(INTEGER(1), nullable=False, server_default=text("'1'"))
#     issued_when = Column(INTEGER(4), nullable=False, server_default=text("'0'"))
#     issued_to = Column(String(16), nullable=False, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))

#     user = relationship('TapirUsers')


# class OrcidIds(Base):
#     __tablename__ = 'arXiv_orcid_ids'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True)
#     orcid = Column(String(19), nullable=False, index=True)
#     authenticated = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

#     user = relationship('TapirUsers', uselist=False)


# class QueueView(Base):
#     __tablename__ = 'arXiv_queue_view'

#     user_id = Column(ForeignKey('tapir_users.user_id', ondelete='CASCADE'), primary_key=True, server_default=text("'0'"))
#     last_view = Column(DateTime)
#     second_last_view = Column(DateTime)
#     total_views = Column(INTEGER(3), nullable=False, server_default=text("'0'"))

#     user = relationship('TapirUsers', uselist=False)


# class SuspiciousNames(Base):
#     __tablename__ = 'arXiv_suspicious_names'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
#     full_name = Column(String(255), nullable=False, server_default=text("''"))

#     user = relationship('TapirUsers', uselist=False)


# class SwordLicenses(Base):
#     __tablename__ = 'arXiv_sword_licenses'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True)
#     license = Column(String(127))
#     updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

#     user = relationship('TapirUsers', uselist=False)


# class TapirAddress(Base):
#     __tablename__ = 'tapir_address'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     address_type = Column(INTEGER(1), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
#     company = Column(String(80), nullable=False, server_default=text("''"))
#     line1 = Column(String(80), nullable=False, server_default=text("''"))
#     line2 = Column(String(80), nullable=False, server_default=text("''"))
#     city = Column(String(50), nullable=False, index=True, server_default=text("''"))
#     state = Column(String(50), nullable=False, server_default=text("''"))
#     postal_code = Column(String(16), nullable=False, index=True, server_default=text("''"))
#     country = Column(ForeignKey('tapir_countries.digraph'), nullable=False, index=True, server_default=text("''"))
#     share_addr = Column(INTEGER(1), nullable=False, server_default=text("'0'"))

#     tapir_countries = relationship('TapirCountries')
#     user = relationship('TapirUsers')


# class TapirDemographics(Base):
#     __tablename__ = 'tapir_demographics'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
#     gender = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     share_gender = Column(INTEGER(1), nullable=False, server_default=text("'16'"))
#     birthday = Column(Date, index=True)
#     share_birthday = Column(INTEGER(1), nullable=False, server_default=text("'16'"))
#     country = Column(ForeignKey('tapir_countries.digraph'), nullable=False, index=True, server_default=text("''"))
#     share_country = Column(INTEGER(1), nullable=False, server_default=text("'16'"))
#     postal_code = Column(String(16), nullable=False, index=True, server_default=text("''"))

#     tapir_countries = relationship('TapirCountries')
#     user = relationship('TapirUsers', uselist=False)


# class TapirEmailChangeTokens(Base):
#     __tablename__ = 'tapir_email_change_tokens'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     old_email = Column(String(50), nullable=False, server_default=text("''"))
#     new_email = Column(String(50), nullable=False, server_default=text("''"))
#     secret = Column(String(32), primary_key=True, nullable=False, index=True, server_default=text("''"))
#     tapir_dest = Column(String(255), nullable=False, server_default=text("''"))
#     issued_when = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     issued_to = Column(String(16), nullable=False, server_default=text("''"))
#     remote_host = Column(String(16), nullable=False, server_default=text("''"))
#     tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
#     used = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     session_id = Column(INTEGER(4), nullable=False, server_default=text("'0'"))
#     consumed_when = Column(INTEGER(10))
#     consumed_from = Column(String(16))

#     user = relationship('TapirUsers')


# class TapirEmailTemplates(Base):
#     __tablename__ = 'tapir_email_templates'
#     __table_args__ = (
#         Index('short_name', 'short_name', 'lang', unique=True),
#     )

#     template_id = Column(INTEGER(10), primary_key=True)
#     short_name = Column(String(32), nullable=False, server_default=text("''"))
#     lang = Column(CHAR(2), nullable=False, server_default=text("'en'"))
#     long_name = Column(String(255), nullable=False, server_default=text("''"))
#     data = Column(Text, nullable=False)
#     sql_statement = Column(Text, nullable=False)
#     update_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     created_by = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     updated_by = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     workflow_status = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     flag_system = Column(INTEGER(1), nullable=False, server_default=text("'0'"))

#     tapir_users = relationship('TapirUsers', primaryjoin='TapirEmailTemplates.created_by == TapirUsers.user_id')
#     tapir_users1 = relationship('TapirUsers', primaryjoin='TapirEmailTemplates.updated_by == TapirUsers.user_id')


# class TapirEmailTokens(Base):
#     __tablename__ = 'tapir_email_tokens'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     secret = Column(String(32), primary_key=True, nullable=False, index=True, server_default=text("''"))
#     tapir_dest = Column(String(255), nullable=False, server_default=text("''"))
#     issued_when = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     issued_to = Column(String(16), nullable=False, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
#     wants_perm_token = Column(INTEGER(1), nullable=False, server_default=text("'0'"))

#     user = relationship('TapirUsers')


# class TapirNicknames(Base):
#     __tablename__ = 'tapir_nicknames'
#     __table_args__ = (
#         Index('user_id', 'user_id', 'user_seq', unique=True),
#     )

#     nick_id = Column(INTEGER(10), primary_key=True)
#     nickname = Column(String(20), nullable=False, unique=True, server_default=text("''"))
#     user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, server_default=text("'0'"))
#     user_seq = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     flag_valid = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     role = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     policy = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     flag_primary = Column(INTEGER(1), nullable=False, server_default=text("'0'"))

#     user = relationship('TapirUsers')


# class TapirPhone(Base):
#     __tablename__ = 'tapir_phone'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     phone_type = Column(INTEGER(1), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
#     phone_number = Column(String(32), index=True)
#     share_phone = Column(INTEGER(1), nullable=False, server_default=text("'16'"))

#     user = relationship('TapirUsers')


# class TapirRecoveryTokens(Base):
#     __tablename__ = 'tapir_recovery_tokens'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     secret = Column(String(32), primary_key=True, nullable=False, index=True, server_default=text("''"))
#     valid = Column(INTEGER(1), nullable=False, server_default=text("'1'"))
#     tapir_dest = Column(String(255), nullable=False, server_default=text("''"))
#     issued_when = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     issued_to = Column(String(16), nullable=False, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))

#     user = relationship('TapirUsers')


# class TapirSessions(Base):
#     __tablename__ = 'tapir_sessions'

#     session_id = Column(INTEGER(4), primary_key=True)
#     user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     last_reissue = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
#     start_time = Column(INTEGER(11), nullable=False, index=True, server_default=text("'0'"))
#     end_time = Column(INTEGER(11), nullable=False, index=True, server_default=text("'0'"))

#     user = relationship('TapirUsers')


# class TapirUsersHot(Base):
#     __tablename__ = 'tapir_users_hot'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
#     last_login = Column(INTEGER(4), nullable=False, index=True, server_default=text("'0'"))
#     second_last_login = Column(INTEGER(4), nullable=False, index=True, server_default=text("'0'"))
#     number_sessions = Column(INTEGER(4), nullable=False, index=True, server_default=text("'0'"))

#     user = relationship('TapirUsers', uselist=False)


# class TapirUsersPassword(Base):
#     __tablename__ = 'tapir_users_password'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
#     password_storage = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     password_enc = Column(String(50), nullable=False, server_default=text("''"))

#     user = relationship('TapirUsers', uselist=False)


# class AdminMetadata(Base):
#     __tablename__ = 'arXiv_admin_metadata'
#     __table_args__ = (
#         Index('pidv', 'paper_id', 'version', unique=True),
#     )

#     metadata_id = Column(INTEGER(11), primary_key=True, index=True)
#     document_id = Column(ForeignKey('arXiv_documents.document_id', ondelete='CASCADE'), index=True)
#     paper_id = Column(String(64))
#     created = Column(DateTime)
#     updated = Column(DateTime)
#     submitter_name = Column(String(64))
#     submitter_email = Column(String(64))
#     history = Column(Text)
#     source_size = Column(INTEGER(11))
#     source_type = Column(String(12))
#     title = Column(Text)
#     authors = Column(Text)
#     category_string = Column(String(255))
#     comments = Column(Text)
#     proxy = Column(String(255))
#     report_num = Column(Text)
#     msc_class = Column(String(255))
#     acm_class = Column(String(255))
#     journal_ref = Column(Text)
#     doi = Column(String(255))
#     abstract = Column(Text)
#     license = Column(String(255))
#     version = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
#     modtime = Column(INTEGER(10))
#     is_current = Column(TINYINT(1), server_default=text("'0'"))

#     document = relationship('Documents')


# t_arXiv_bogus_subject_class = Table(
#     'arXiv_bogus_subject_class', metadata,
#     Column('document_id', ForeignKey('arXiv_documents.document_id'), nullable=False, index=True, server_default=text("'0'")),
#     Column('category_name', String(255), nullable=False, server_default=text("''"))
# )


# class CategoryDef(Base):
#     __tablename__ = 'arXiv_category_def'
#     __table_args__ = (
#         ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
#         Index('cat_def_fk', 'archive', 'subject_class')
#     )

#     category = Column(String(32), primary_key=True)
#     name = Column(String(255))
#     active = Column(TINYINT(1), server_default=text("'1'"))
#     archive = Column(String(16), nullable=False, server_default=text("''"))
#     subject_class = Column(String(16), nullable=False, server_default=text("''"))

#     arXiv_categories = relationship('Categories')


# class CrossControl(Base):
#     __tablename__ = 'arXiv_cross_control'
#     __table_args__ = (
#         ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
#         Index('archive', 'archive', 'subject_class'),
#         Index('document_id', 'document_id', 'version')
#     )

#     control_id = Column(INTEGER(10), primary_key=True)
#     document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, server_default=text("'0'"))
#     version = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
#     desired_order = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
#     user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     status = Column(Enum('new', 'frozen', 'published', 'rejected'), nullable=False, index=True, server_default=text("'new'"))
#     flag_must_notify = Column(Enum('0', '1'), server_default=text("'1'"))
#     archive = Column(String(16), nullable=False, server_default=text("''"))
#     subject_class = Column(String(16), nullable=False, server_default=text("''"))
#     request_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     freeze_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     publish_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))

#     arXiv_categories = relationship('Categories')
#     document = relationship('Documents')
#     user = relationship('TapirUsers')


# class Dblp(Base):
#     __tablename__ = 'arXiv_dblp'

#     document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, server_default=text("'0'"))
#     url = Column(String(80))

#     document = relationship('Documents', uselist=False)


# class DblpDocumentAuthors(Base):
#     __tablename__ = 'arXiv_dblp_document_authors'

#     document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, nullable=False, index=True)
#     author_id = Column(ForeignKey('arXiv_dblp_authors.author_id'), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
#     position = Column(TINYINT(4), nullable=False, server_default=text("'0'"))

#     author = relationship('DblpAuthors')
#     document = relationship('Documents')


# class Demographics(Base):
#     __tablename__ = 'arXiv_demographics'
#     __table_args__ = (
#         ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
#         Index('archive', 'archive', 'subject_class')
#     )

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
#     country = Column(CHAR(2), nullable=False, index=True, server_default=text("''"))
#     affiliation = Column(String(255), nullable=False, server_default=text("''"))
#     url = Column(String(255), nullable=False, server_default=text("''"))
#     type = Column(SMALLINT(5), index=True)
#     archive = Column(String(16))
#     subject_class = Column(String(16))
#     original_subject_classes = Column(String(255), nullable=False, server_default=text("''"))
#     flag_group_physics = Column(INTEGER(1), index=True)
#     flag_group_math = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_group_cs = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_group_nlin = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_proxy = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_journal = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_xml = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     dirty = Column(INTEGER(1), nullable=False, server_default=text("'2'"))
#     flag_group_test = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     flag_suspect = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_group_q_bio = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_group_q_fin = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_group_stat = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_group_eess = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     flag_group_econ = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
#     veto_status = Column(Enum('ok', 'no-endorse', 'no-upload', 'no-replace'), nullable=False, server_default=text("'ok'"))

#     arXiv_categories = relationship('Categories')
#     user = relationship('TapirUsers', uselist=False, viewonly=True)


# class EndorsementRequests(Base):
#     __tablename__ = 'arXiv_endorsement_requests'
#     __table_args__ = (
#         ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
#         Index('archive', 'archive', 'subject_class'),
#         Index('endorsee_id_2', 'endorsee_id', 'archive', 'subject_class', unique=True)
#     )

#     request_id = Column(INTEGER(10), primary_key=True)
#     endorsee_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     archive = Column(String(16), nullable=False, server_default=text("''"))
#     subject_class = Column(String(16), nullable=False, server_default=text("''"))
#     secret = Column(String(16), nullable=False, unique=True, server_default=text("''"))
#     flag_valid = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     issued_when = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     point_value = Column(INTEGER(10), nullable=False, server_default=text("'0'"))

#     arXiv_categories = relationship('Categories')
#     endorsee = relationship('TapirUsers')


# t_arXiv_in_category = Table(
#     'arXiv_in_category', metadata,
#     Column('document_id', ForeignKey('arXiv_documents.document_id'), nullable=False, index=True, server_default=text("'0'")),
#     Column('archive', String(16), nullable=False, server_default=text("''")),
#     Column('subject_class', String(16), nullable=False, server_default=text("''")),
#     Column('is_primary', TINYINT(1), nullable=False, server_default=text("'0'")),
#     ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
#     Index('archive', 'archive', 'subject_class', 'document_id', unique=True),
#     Index('arXiv_in_category_mp', 'archive', 'subject_class')
# )


# class JrefControl(Base):
#     __tablename__ = 'arXiv_jref_control'
#     __table_args__ = (
#         Index('document_id', 'document_id', 'version', unique=True),
#     )

#     control_id = Column(INTEGER(10), primary_key=True)
#     document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, server_default=text("'0'"))
#     version = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
#     user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     status = Column(Enum('new', 'frozen', 'published', 'rejected'), nullable=False, index=True, server_default=text("'new'"))
#     flag_must_notify = Column(Enum('0', '1'), server_default=text("'1'"))
#     jref = Column(String(255), nullable=False, server_default=text("''"))
#     request_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     freeze_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     publish_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))

#     document = relationship('Documents')
#     user = relationship('TapirUsers')


# class Metadata(Base):
#     __tablename__ = 'arXiv_metadata'
#     __table_args__ = (
#         Index('pidv', 'paper_id', 'version', unique=True),
#     )

#     metadata_id = Column(INTEGER(11), primary_key=True)
#     document_id = Column(ForeignKey('arXiv_documents.document_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'0'"))
#     paper_id = Column(String(64), nullable=False)
#     created = Column(DateTime)
#     updated = Column(DateTime)
#     submitter_id = Column(ForeignKey('tapir_users.user_id'), index=True)
#     submitter_name = Column(String(64), nullable=False)
#     submitter_email = Column(String(64), nullable=False)
#     source_size = Column(INTEGER(11))
#     source_format = Column(String(12))
#     source_flags = Column(String(12))
#     title = Column(Text)
#     authors = Column(Text)
#     abs_categories = Column(String(255))
#     comments = Column(Text)
#     proxy = Column(String(255))
#     report_num = Column(Text)
#     msc_class = Column(String(255))
#     acm_class = Column(String(255))
#     journal_ref = Column(Text)
#     doi = Column(String(255))
#     abstract = Column(Text)
#     license = Column(ForeignKey('arXiv_licenses.name'), index=True)
#     version = Column(INTEGER(4), nullable=False, server_default=text("'1'"))
#     modtime = Column(INTEGER(11))
#     is_current = Column(TINYINT(1), server_default=text("'1'"))
#     is_withdrawn = Column(TINYINT(1), nullable=False, server_default=text("'0'"))

#     document = relationship('Documents')
#     arXiv_licenses = relationship('Licenses')
#     submitter = relationship('TapirUsers')


# class MirrorList(Base):
#     __tablename__ = 'arXiv_mirror_list'

#     mirror_list_id = Column(INTEGER(11), primary_key=True)
#     created = Column(DateTime)
#     updated = Column(DateTime)
#     document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, index=True, server_default=text("'0'"))
#     version = Column(INTEGER(4), nullable=False, server_default=text("'1'"))
#     write_source = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     write_abs = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     is_written = Column(TINYINT(1), nullable=False, server_default=text("'0'"))

#     document = relationship('Documents')


# t_arXiv_moderators = Table(
#     'arXiv_moderators', metadata,
#     Column('user_id', ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'")),
#     Column('archive', ForeignKey('arXiv_archive_group.archive_id'), nullable=False, server_default=text("''")),
#     Column('subject_class', String(16), nullable=False, server_default=text("''")),
#     Column('is_public', TINYINT(4), nullable=False, server_default=text("'0'")),
#     Column('no_email', TINYINT(1), index=True, server_default=text("'0'")),
#     Column('no_web_email', TINYINT(1), index=True, server_default=text("'0'")),
#     Column('no_reply_to', TINYINT(1), index=True, server_default=text("'0'")),
#     Column('daily_update', TINYINT(1), server_default=text("'0'")),
#     ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
#     Index('user_id', 'archive', 'subject_class', 'user_id', unique=True)
# )


# t_arXiv_paper_owners = Table(
#     'arXiv_paper_owners', metadata,
#     Column('document_id', ForeignKey('arXiv_documents.document_id'), nullable=False, server_default=text("'0'")),
#     Column('user_id', ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'")),
#     Column('date', INTEGER(10), nullable=False, server_default=text("'0'")),
#     Column('added_by', ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'")),
#     Column('remote_addr', String(16), nullable=False, server_default=text("''")),
#     Column('remote_host', String(255), nullable=False, server_default=text("''")),
#     Column('tracking_cookie', String(32), nullable=False, server_default=text("''")),
#     Column('valid', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_author', INTEGER(1), nullable=False, server_default=text("'0'")),
#     Column('flag_auto', INTEGER(1), nullable=False, server_default=text("'1'")),
#     Index('document_id', 'document_id', 'user_id', unique=True)
# )


# class PaperPw(Base):
#     __tablename__ = 'arXiv_paper_pw'

#     document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, server_default=text("'0'"))
#     password_storage = Column(INTEGER(1))
#     password_enc = Column(String(50))

#     document = relationship('Documents', uselist=False)


# class QuestionableCategories(Base):
#     __tablename__ = 'arXiv_questionable_categories'
#     __table_args__ = (
#         ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
#     )

#     archive = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
#     subject_class = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))

#     arXiv_categories = relationship('Categories', uselist=False)


# class ShowEmailRequests(Base):
#     __tablename__ = 'arXiv_show_email_requests'
#     __table_args__ = (
#         Index('user_id', 'user_id', 'dated'),
#     )

#     document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, index=True, server_default=text("'0'"))
#     user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, server_default=text("'0'"))
#     session_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     dated = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     flag_allowed = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
#     remote_addr = Column(String(16), nullable=False, index=True, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
#     request_id = Column(INTEGER(10), primary_key=True)

#     document = relationship('Documents')
#     user = relationship('TapirUsers')


# class SubmissionControl(Base):
#     __tablename__ = 'arXiv_submission_control'
#     __table_args__ = (
#         Index('document_id', 'document_id', 'version', unique=True),
#     )

#     control_id = Column(INTEGER(10), primary_key=True)
#     document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, server_default=text("'0'"))
#     version = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
#     pending_paper_id = Column(String(20), nullable=False, index=True, server_default=text("''"))
#     user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     status = Column(Enum('new', 'frozen', 'published', 'rejected'), nullable=False, index=True, server_default=text("'new'"))
#     flag_must_notify = Column(Enum('0', '1'), server_default=text("'1'"))
#     request_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     freeze_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     publish_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))

#     document = relationship('Documents')
#     user = relationship('TapirUsers')


# class Submissions(Base):
#     __tablename__ = 'arXiv_submissions'

#     submission_id = Column(INTEGER(11), primary_key=True)
#     document_id = Column(ForeignKey('arXiv_documents.document_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
#     doc_paper_id = Column(VARCHAR(20), index=True)
#     sword_id = Column(ForeignKey('arXiv_tracking.sword_id'), index=True)
#     userinfo = Column(TINYINT(4), server_default=text("'0'"))
#     is_author = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     agree_policy = Column(TINYINT(1), server_default=text("'0'"))
#     viewed = Column(TINYINT(1), server_default=text("'0'"))
#     stage = Column(INTEGER(11), server_default=text("'0'"))
#     submitter_id = Column(ForeignKey('tapir_users.user_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
#     submitter_name = Column(String(64))
#     submitter_email = Column(String(64))
#     created = Column(DateTime)
#     updated = Column(DateTime)
#     status = Column(INTEGER(11), nullable=False, index=True, server_default=text("'0'"))
#     sticky_status = Column(INTEGER(11))
#     must_process = Column(TINYINT(1), server_default=text("'1'"))
#     submit_time = Column(DateTime)
#     release_time = Column(DateTime)
#     source_size = Column(INTEGER(11), server_default=text("'0'"))
#     source_format = Column(VARCHAR(12))
#     source_flags = Column(VARCHAR(12))
#     has_pilot_data = Column(TINYINT(1))
#     is_withdrawn = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     title = Column(Text)
#     authors = Column(Text)
#     comments = Column(Text)
#     proxy = Column(VARCHAR(255))
#     report_num = Column(Text)
#     msc_class = Column(String(255))
#     acm_class = Column(String(255))
#     journal_ref = Column(Text)
#     doi = Column(String(255))
#     abstract = Column(Text)
#     license = Column(ForeignKey('arXiv_licenses.name', onupdate='CASCADE'), index=True)
#     version = Column(INTEGER(4), nullable=False, server_default=text("'1'"))
#     type = Column(CHAR(8), index=True)
#     is_ok = Column(TINYINT(1), index=True)
#     admin_ok = Column(TINYINT(1))
#     allow_tex_produced = Column(TINYINT(1), server_default=text("'0'"))
#     is_oversize = Column(TINYINT(1), server_default=text("'0'"))
#     remote_addr = Column(VARCHAR(16), nullable=False, server_default=text("''"))
#     remote_host = Column(VARCHAR(255), nullable=False, server_default=text("''"))
#     package = Column(VARCHAR(255), nullable=False, server_default=text("''"))
#     rt_ticket_id = Column(INTEGER(8), index=True)
#     auto_hold = Column(TINYINT(1), server_default=text("'0'"))
#     is_locked = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))

#     document = relationship('Documents')
#     arXiv_licenses = relationship('Licenses')
#     submitter = relationship('TapirUsers')
#     sword = relationship('Tracking')
#     submission_category = relationship('SubmissionCategory', viewonly=True)
#     abs_classifier_data = relationship('SubmissionAbsClassifierData', viewonly=True)
#     proposals = relationship('SubmissionCategoryProposal', viewonly=True)
#     hold_reasons = relationship('SubmissionHoldReason', viewonly=True)
#     flags = relationship('SubmissionFlag', viewonly=True)
#     admin_log = relationship('AdminLog',
#                              primaryjoin='AdminLog.submission_id == Submissions.submission_id',
#                              foreign_keys='AdminLog.submission_id',
#                              collection_class=list)

#     @property
#     def primary_classification(self) -> Optional[str]:
#         """Get the primary classification for this submission."""
#         categories = [
#             db_cat for db_cat in self.submission_category if db_cat.is_primary == 1
#         ]
#         try:
#             cat = categories[0].category
#         except Exception:
#             return None
#         return cat

#     @property
#     def secondary_categories(self) -> List[str]:
#         """Category names from this submission's secondary classifications.

#         Returns published and unpublished secondaries."""
#         return [c.category for c in self.submission_category
#                 if c.is_primary == 0]

#     @property
#     def categories(self) -> List[str]:
#         """All the categories"""
#         return [cr.category for cr in self.submission_category]

#     @property
#     def new_crosses(self) -> List[str]:
#         """For type 'new' these will be redundant with secondary_categories"""
#         return [c.category for c in self.submission_category
#                 if c.is_primary == 0 and c.is_published != 1]

#     @property
#     def hold_reason(self) -> Optional['SubmissionHoldReason']:
#         if self.hold_reasons:
#             return self.hold_reasons[0]
#         else:
#             return None

#     @property
#     def fudged_categories(self) -> str:

#         # This is a close port of the legacy code
#         # Needs to be same as arXiv::Schema::ResultSet::DocCategory.string
#         primary_str = self.primary_classification if self.primary_classification else '-'
#         secondary_list = list(set([cat for cat in self.secondary_categories]))
#         cats_to_add = [CATEGORY_ALIASES_INV[cat] for cat in secondary_list
#                        if cat in CATEGORY_ALIASES_INV]
#         fudged = [primary_str] + sorted(secondary_list + cats_to_add)
#         return ' '.join(fudged)

# class TopPapers(Base):
#     __tablename__ = 'arXiv_top_papers'

#     from_week = Column(Date, primary_key=True, nullable=False, server_default=text("'0000-00-00'"))
#     _class = Column('class', CHAR(1), primary_key=True, nullable=False, server_default=text("''"))
#     rank = Column(SMALLINT(5), primary_key=True, nullable=False, server_default=text("'0'"))
#     document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, index=True, server_default=text("'0'"))
#     viewers = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))

#     document = relationship('Documents')


# class Versions(Base):
#     __tablename__ = 'arXiv_versions'

#     document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     version = Column(TINYINT(3), primary_key=True, nullable=False, server_default=text("'0'"))
#     request_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     freeze_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     publish_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     flag_current = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))

#     document = relationship('Documents')


# class TapirAdminAudit(Base):
#     __tablename__ = 'tapir_admin_audit'

#     log_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     session_id = Column(ForeignKey('tapir_sessions.session_id'), index=True)
#     ip_addr = Column(String(16), nullable=False, index=True, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     admin_user = Column(ForeignKey('tapir_users.user_id'), index=True)
#     affected_user = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
#     action = Column(String(32), nullable=False, server_default=text("''"))
#     data = Column(Text, nullable=False, index=True)
#     comment = Column(Text, nullable=False)
#     entry_id = Column(INTEGER(10), primary_key=True)

#     tapir_users = relationship('TapirUsers', primaryjoin='TapirAdminAudit.admin_user == TapirUsers.user_id')
#     tapir_users1 = relationship('TapirUsers', primaryjoin='TapirAdminAudit.affected_user == TapirUsers.user_id')
#     session = relationship('TapirSessions')


# t_tapir_email_change_tokens_used = Table(
#     'tapir_email_change_tokens_used', metadata,
#     Column('user_id', ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'")),
#     Column('secret', String(32), nullable=False, server_default=text("''")),
#     Column('used_when', INTEGER(10), nullable=False, server_default=text("'0'")),
#     Column('used_from', String(16), nullable=False, server_default=text("''")),
#     Column('remote_host', String(255), nullable=False, server_default=text("''")),
#     Column('session_id', ForeignKey('tapir_sessions.session_id'), nullable=False, index=True, server_default=text("'0'"))
# )


# class TapirEmailHeaders(Base):
#     __tablename__ = 'tapir_email_headers'

#     template_id = Column(ForeignKey('tapir_email_templates.template_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     header_name = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
#     header_content = Column(String(255), nullable=False, server_default=text("''"))

#     template = relationship('TapirEmailTemplates')


# class TapirEmailMailings(Base):
#     __tablename__ = 'tapir_email_mailings'

#     mailing_id = Column(INTEGER(10), primary_key=True)
#     template_id = Column(ForeignKey('tapir_email_templates.template_id'), index=True)
#     created_by = Column(ForeignKey('tapir_users.user_id'), index=True)
#     sent_by = Column(ForeignKey('tapir_users.user_id'), index=True)
#     created_date = Column(INTEGER(10))
#     sent_date = Column(INTEGER(10))
#     complete_date = Column(INTEGER(10))
#     mailing_name = Column(String(255))
#     comment = Column(Text)

#     tapir_users = relationship('TapirUsers', primaryjoin='TapirEmailMailings.created_by == TapirUsers.user_id')
#     tapir_users1 = relationship('TapirUsers', primaryjoin='TapirEmailMailings.sent_by == TapirUsers.user_id')
#     template = relationship('TapirEmailTemplates')


# t_tapir_email_tokens_used = Table(
#     'tapir_email_tokens_used', metadata,
#     Column('user_id', ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'")),
#     Column('secret', String(32), nullable=False, server_default=text("''")),
#     Column('used_when', INTEGER(10), nullable=False, server_default=text("'0'")),
#     Column('used_from', String(16), nullable=False, server_default=text("''")),
#     Column('remote_host', String(255), nullable=False, server_default=text("''")),
#     Column('session_id', ForeignKey('tapir_sessions.session_id'), nullable=False, index=True, server_default=text("'0'"))
# )


# class TapirPermanentTokens(Base):
#     __tablename__ = 'tapir_permanent_tokens'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
#     valid = Column(INTEGER(1), nullable=False, server_default=text("'1'"))
#     issued_when = Column(INTEGER(4), nullable=False, server_default=text("'0'"))
#     issued_to = Column(String(16), nullable=False, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     session_id = Column(ForeignKey('tapir_sessions.session_id'), nullable=False, index=True, server_default=text("'0'"))

#     session = relationship('TapirSessions')
#     user = relationship('TapirUsers')


# t_tapir_permanent_tokens_used = Table(
#     'tapir_permanent_tokens_used', metadata,
#     Column('user_id', ForeignKey('tapir_users.user_id'), index=True),
#     Column('secret', String(32), nullable=False, server_default=text("''")),
#     Column('used_when', INTEGER(4)),
#     Column('used_from', String(16)),
#     Column('remote_host', String(255), nullable=False, server_default=text("''")),
#     Column('session_id', ForeignKey('tapir_sessions.session_id'), nullable=False, index=True, server_default=text("'0'"))
# )


# class TapirRecoveryTokensUsed(Base):
#     __tablename__ = 'tapir_recovery_tokens_used'

#     user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
#     secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
#     used_when = Column(INTEGER(4))
#     used_from = Column(String(16))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     session_id = Column(ForeignKey('tapir_sessions.session_id'), index=True)

#     session = relationship('TapirSessions')
#     user = relationship('TapirUsers')


# class TapirSessionsAudit(Base):
#     __tablename__ = 'tapir_sessions_audit'

#     session_id = Column(ForeignKey('tapir_sessions.session_id'), primary_key=True, server_default=text("'0'"))
#     ip_addr = Column(String(16), nullable=False, index=True, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     tracking_cookie = Column(String(255), nullable=False, index=True, server_default=text("''"))

#     session = relationship('TapirSessions', uselist=False)


# class DocumentCategory(Base):
#     __tablename__ = 'arXiv_document_category'

#     document_id = Column(ForeignKey('arXiv_documents.document_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
#     category = Column(ForeignKey('arXiv_category_def.category'), primary_key=True, nullable=False, index=True)
#     is_primary = Column(TINYINT(1), nullable=False, server_default=text("'0'"))

#     arXiv_category_def = relationship('CategoryDef')
#     document = relationship('Documents')


# class EndorsementRequestsAudit(Base):
#     __tablename__ = 'arXiv_endorsement_requests_audit'

#     request_id = Column(ForeignKey('arXiv_endorsement_requests.request_id'), primary_key=True, server_default=text("'0'"))
#     session_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     remote_addr = Column(String(16))
#     remote_host = Column(String(255))
#     tracking_cookie = Column(String(255))

#     request = relationship('EndorsementRequests', uselist=False)


# class Endorsements(Base):
#     __tablename__ = 'arXiv_endorsements'
#     __table_args__ = (
#         ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
#         Index('endorser_id_2', 'endorser_id', 'endorsee_id', 'archive', 'subject_class', unique=True),
#         Index('archive', 'archive', 'subject_class')
#     )

#     endorsement_id = Column(INTEGER(10), primary_key=True)
#     endorser_id = Column(ForeignKey('tapir_users.user_id'), index=True)
#     endorsee_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     archive = Column(String(16), nullable=False, server_default=text("''"))
#     subject_class = Column(String(16), nullable=False, server_default=text("''"))
#     flag_valid = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     type = Column(Enum('user', 'admin', 'auto'))
#     point_value = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     issued_when = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     request_id = Column(ForeignKey('arXiv_endorsement_requests.request_id'), index=True)

#     arXiv_categories = relationship('Categories')
#     endorsee = relationship('TapirUsers', primaryjoin='Endorsements.endorsee_id == TapirUsers.user_id')
#     endorser = relationship('TapirUsers', primaryjoin='Endorsements.endorser_id == TapirUsers.user_id')
#     request = relationship('EndorsementRequests')


# class OwnershipRequests(Base):
#     __tablename__ = 'arXiv_ownership_requests'

#     request_id = Column(INTEGER(10), primary_key=True)
#     user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
#     endorsement_request_id = Column(ForeignKey('arXiv_endorsement_requests.request_id'), index=True)
#     workflow_status = Column(Enum('pending', 'accepted', 'rejected'), nullable=False, server_default=text("'pending'"))

#     endorsement_request = relationship('EndorsementRequests')
#     user = relationship('TapirUsers')


# class PilotDatasets(Base):
#     __tablename__ = 'arXiv_pilot_datasets'

#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id'), primary_key=True)
#     numfiles = Column(SMALLINT(4), server_default=text("'0'"))
#     feed_url = Column(String(256))
#     manifestation = Column(String(256))
#     published = Column(TINYINT(1), server_default=text("'0'"))
#     created = Column(DateTime, nullable=False)
#     last_checked = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

#     submission = relationship('Submissions', uselist=False)


# class PilotFiles(Base):
#     __tablename__ = 'arXiv_pilot_files'

#     file_id = Column(INTEGER(11), primary_key=True)
#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id'), nullable=False, index=True)
#     filename = Column(String(256), server_default=text("''"))
#     entity_url = Column(String(256))
#     description = Column(String(80))
#     byRef = Column(TINYINT(1), server_default=text("'1'"))

#     submission = relationship('Submissions')


# class SubmissionAbsClassifierData(Base):
#     __tablename__ = 'arXiv_submission_abs_classifier_data'

#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True, server_default=text("'0'"))
#     json = Column(Text)
#     last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#     status = Column(Enum('processing', 'success', 'failed', 'no connection'))
#     message = Column(Text)
#     is_oversize = Column(TINYINT(1), server_default=text("'0'"))
#     suggested_primary = Column(Text)
#     suggested_reason = Column(Text)
#     autoproposal_primary = Column(Text)
#     autoproposal_reason = Column(Text)
#     classifier_service_version = Column(Text)
#     classifier_model_version = Column(Text)

#     submission = relationship('Submissions', uselist=False)


# class SubmissionCategory(Base):
#     __tablename__ = 'arXiv_submission_category'

#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
#     category = Column(ForeignKey('arXiv_category_def.category'), primary_key=True, nullable=False, index=True, server_default=text("''"))
#     is_primary = Column(TINYINT(1), nullable=False, index=True, server_default=text("'0'"))
#     is_published = Column(TINYINT(1), index=True, server_default=text("'0'"))

#     arXiv_category_def = relationship('CategoryDef')
#     submission = relationship('Submissions')


# class SubmissionCategoryProposal(Base):
#     __tablename__ = 'arXiv_submission_category_proposal'

#     proposal_id = Column(INTEGER(11), primary_key=True, nullable=False, index=True, autoincrement=True)
#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
#     category = Column(ForeignKey('arXiv_category_def.category'), primary_key=True, nullable=False, index=True)
#     is_primary = Column(TINYINT(1), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
#     proposal_status = Column(INTEGER(11), server_default=text("'0'"))
#     user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True)
#     updated = Column(DateTime)
#     proposal_comment_id = Column(ForeignKey('arXiv_admin_log.id'), index=True)
#     response_comment_id = Column(ForeignKey('arXiv_admin_log.id'), index=True)

#     arXiv_category_def = relationship('CategoryDef')
#     proposal_comment = relationship('AdminLog', primaryjoin='SubmissionCategoryProposal.proposal_comment_id == AdminLog.id')
#     response_comment = relationship('AdminLog', primaryjoin='SubmissionCategoryProposal.response_comment_id == AdminLog.id')
#     submission = relationship('Submissions')
#     user = relationship('TapirUsers')


# class SubmissionClassifierData(Base):
#     __tablename__ = 'arXiv_submission_classifier_data'

#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True, server_default=text("'0'"))
#     json = Column(Text)
#     last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#     status = Column(Enum('processing', 'success', 'failed', 'no connection'))
#     message = Column(Text)
#     is_oversize = Column(TINYINT(1), server_default=text("'0'"))

#     submission = relationship('Submissions', uselist=False)


# class SubmissionFlag(Base):
#     __tablename__ = 'arXiv_submission_flag'
#     __table_args__ = (
#         Index('uniq_one_flag_per_mod', 'submission_id', 'user_id', unique=True),
#     )

#     flag_id = Column(INTEGER(11), primary_key=True)
#     user_id = Column(ForeignKey('tapir_users.user_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("'0'"))
#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), nullable=False)
#     flag = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
#     updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

#     submission = relationship('Submissions')
#     user = relationship('TapirUsers')


# class SubmissionHoldReason(Base):
#     __tablename__ = 'arXiv_submission_hold_reason'

#     reason_id = Column(INTEGER(11), primary_key=True)
#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), nullable=False, index=True)
#     user_id = Column(ForeignKey('tapir_users.user_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("'0'"))
#     reason = Column(String(30))
#     type = Column(String(30))
#     comment_id = Column(ForeignKey('arXiv_admin_log.id'), index=True)

#     comment = relationship('AdminLog')
#     submission = relationship('Submissions')
#     user = relationship('TapirUsers')


# class SubmissionModHold(Base):
#     __tablename__ = 'arXiv_submission_mod_hold'

#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True)
#     reason = Column(String(30))
#     comment_id = Column(ForeignKey('arXiv_admin_log.id'), nullable=False, index=True)

#     comment = relationship('AdminLog')
#     submission = relationship('Submissions', uselist=False)


# class SubmissionNearDuplicates(Base):
#     __tablename__ = 'arXiv_submission_near_duplicates'
#     __table_args__ = (
#         Index('match', 'submission_id', 'matching_id', unique=True),
#     )

#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True, nullable=False, server_default=text("'0'"))
#     matching_id = Column(INTEGER(11), primary_key=True, nullable=False, server_default=text("'0'"))
#     similarity = Column(DECIMAL(2, 1), nullable=False)
#     last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

#     submission = relationship('Submissions')


# class SubmissionViewFlag(Base):
#     __tablename__ = 'arXiv_submission_view_flag'

#     submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True, nullable=False)
#     flag = Column(TINYINT(1), server_default=text("'0'"))
#     user_id = Column(ForeignKey('tapir_users.user_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
#     updated = Column(DateTime)

#     submission = relationship('Submissions')
#     user = relationship('TapirUsers')


# class VersionsChecksum(Base):
#     __tablename__ = 'arXiv_versions_checksum'
#     __table_args__ = (
#         ForeignKeyConstraint(['document_id', 'version'], ['arXiv_versions.document_id', 'arXiv_versions.version']),
#     )

#     document_id = Column(MEDIUMINT(8), primary_key=True, nullable=False, server_default=text("'0'"))
#     version = Column(TINYINT(3), primary_key=True, nullable=False, server_default=text("'0'"))
#     flag_abs_present = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     abs_size = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     abs_md5sum = Column(BINARY(16), index=True)
#     flag_src_present = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
#     src_size = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
#     src_md5sum = Column(BINARY(16), index=True)

#     document = relationship('Versions', uselist=False)


# class EndorsementsAudit(Base):
#     __tablename__ = 'arXiv_endorsements_audit'

#     endorsement_id = Column(ForeignKey('arXiv_endorsements.endorsement_id'), primary_key=True, server_default=text("'0'"))
#     session_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     remote_addr = Column(String(16), nullable=False, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
#     flag_knows_personally = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     flag_seen_paper = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
#     comment = Column(Text)

#     endorsement = relationship('Endorsements', uselist=False)


# class OwnershipRequestsAudit(Base):
#     __tablename__ = 'arXiv_ownership_requests_audit'

#     request_id = Column(ForeignKey('arXiv_ownership_requests.request_id'), primary_key=True, server_default=text("'0'"))
#     session_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
#     remote_addr = Column(String(16), nullable=False, server_default=text("''"))
#     remote_host = Column(String(255), nullable=False, server_default=text("''"))
#     tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
#     date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))

#     request = relationship('OwnershipRequests', uselist=False)
