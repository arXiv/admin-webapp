-- SET FOREIGN_KEY_CHECKS = 0;

-- Tapir Users
INSERT INTO `tapir_users` VALUES (246231,'Brandon','Barker','',1,1,'no-mail@example.com',8,0,2,1384185389,'dedicated','',0,0,0,1,1,0,0,0,0,'cpe-24-59.res.rr.com.1372902602452690',0,0);
INSERT INTO `arXiv_moderators` VALUES (246231,'q-bio','CB','0','0','0','0','0');
INSERT INTO `arXiv_moderators` VALUES (246231,'q-bio','NC','0','0','0','0','0');
INSERT INTO `arXiv_moderators` VALUES (246231,'q-bio', '','0','0','0','0','0');

INSERT INTO `tapir_users` VALUES (246232,'Lo','Jack','',1,1,'other-no-mail@example.com',8,0,2,1384185389,'net','',0,0,0,1,1,0,0,0,0,'cpe-24-59.com.1372902602452690',0,0);
INSERT INTO `arXiv_moderators` VALUES (246232,'q-bio','NC','0','0','0','0','0');

INSERT INTO `tapir_users` VALUES (246233,'Frank','Franky','',1,1,'no-mailx234@example.com',8,0,2,1384185389,'dedicated','',0,0,0,1,1,0,0,0,0,'cpe-24-59.res.rr.com.1372902602452690',0,0);
INSERT INTO `arXiv_moderators` VALUES (246233,'hep-ph', '','0','0','0','0','0');
INSERT INTO `tapir_nicknames` VALUES (246210,'ffrky',246233,1,1,0,0,1);

INSERT INTO `tapir_users` VALUES (9999,'Ralf','W','',1,1,'no-mail-rw@example.com',8,0,2,1384185389,'dedicated','',0,0,0,1,1,0,0,0,0,'',0,0);

INSERT INTO `arXiv_moderators` VALUES (9999, 'astro-ph', '', '0' , '0' , '0' , '0' , '0' );
INSERT INTO `arXiv_moderators` VALUES (9999, 'astro-ph', 'HE', 1 , '0' , '0' , '0' , '0' );
INSERT INTO `arXiv_moderators` VALUES (9999, 'cond-mat', '', '0' , '0' , '0' , '0' , '0' );
INSERT INTO `arXiv_moderators` VALUES (9999, 'physics', '', '0' , '0' , '0' , '0' , '0' );

-- non-mod non-admin user
INSERT INTO `tapir_users` VALUES (1212,'Random','Reader','',1,1,'no-mail-randomreader@example.com',8,0,2,1384185389,'dedicated','',0,0,0,1,1,0,0,0,0,'xyz',0,0);

INSERT INTO `tapir_nicknames` VALUES (241212,'reader',1212,1,1,0,0,1);

-- admin service account user for GCP test
INSERT INTO `tapir_users` VALUES (4455,'Service','account','',1,1,'qa-tools-sa@arxiv-proj.iam.gserviceaccount.com',8,0,2,1384185389,'dedicated','',0,1,0,1,1,0,0,0,0,'xyz',0,0);

INSERT INTO `tapir_nicknames` VALUES (2412,'qaServiceAccount',4455,1,1,0,0,1);

-- Tapir Nicknames
INSERT INTO `tapir_nicknames` VALUES (246208,'bbarker',246231,1,1,0,0,1);
INSERT INTO `tapir_nicknames` VALUES (246209,'lowjack',246232,1,1,0,0,1);
INSERT INTO `tapir_nicknames` VALUES (249999,'ralph',9999,1,1,0,0,1);


-- Submissions
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(1137914,NULL,NULL,NULL,1,1,1,1,4 /* stage */,246231,'Brandon Barker','beb82@cornell.edu','2015-10-12 17:11:21','2015-10-12 21:58:44',1 /* status */,NULL,0,'2015-11-17 15:11:21',NULL,2848951,'pdf','1',0,0,'MPI 3 One more time','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'The Message Passing Interface, version three point zero.','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',NULL,NULL,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/Kubla_Khan.pdf',NULL,0,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (1137914,'q-bio.CB',1,0);


INSERT INTO `arXiv_submission_abs_classifier_data`
( `submission_id`, `json`, `last_update`, `status`, `message`,
`is_oversize`, `suggested_primary`, `suggested_reason`,
`autoproposal_primary`, `autoproposal_reason`,
`classifier_service_version`, `classifier_model_version`)
VALUES(
1137914,
'{"classifier":[{"category":"hep-ph","probability":0.97},{"category":"hep-ex","probability":0.65},{"category":"hep-th","probability":0.02},{"category":"nucl-ex","probability":0.01},{"category":"nucl-th","probability":0.01}],"service":"fb-abs"}',
'2021-04-13 12:49:38', 'success', NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL);

INSERT INTO arXiv_admin_log
(submission_id, username, program, command, logtext)
VALUES
(1137914, 'bbarker', 'Admin::Queue', 'admin comment', 'test comment');

INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(1137933,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-17 15:37:23','2015-11-17 15:11:21',1 /*status*/,NULL,0,NULL,NULL,500,'tex','1',0,0,'A very simple LaTeX example','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'A very simple LaTeX example.','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'10.128.128.241','dhcp-gs-241.eduroam.cornell.edu','/users/e-prints/arXivLib/t/user_data/very_simple_1137933.gz',NULL,0,NULL);


INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (1137933,'q-bio.NC',1,0);


-- Locked submission
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`, is_locked)
VALUES
(100430 ,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-17 15:37:23','2015-11-17 15:11:21',1 /*status*/,NULL,0,'2015-11-17 15:11:21',NULL,500,'tex','1',0,0,'A very simple LaTeX example','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'A very simple LaTeX example.','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'10.128.128.241','dhcp-gs-241.eduroam.cornell.edu','/users/e-prints/arXivLib/t/user_data/very_simple_1137933.gz',NULL,0,NULL, 1);


INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (100430,'q-bio.NC',1,0);



INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(1137931,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-16 18:34:31','2015-11-17 13:37:25',1/*status*/,NULL,0,'2015-11-16 19:50:55',NULL,998628,'pdftex','',0,0,'First timeout fail case','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'First timeout fail case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',NULL,NULL,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137931.tar.gz',NULL,1,NULL);


INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (1137931,'q-bio.GN',1,0);



INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(1137932,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-16 19:58:40','2015-11-17 14:15:41',1,NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'Second timeout test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Second timeout test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,0,NULL);


INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (1137932,'q-bio.GN',1,0);




INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(1137934,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-16 19:58:40','2015-11-17 14:15:41', 1, NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'Second timeout test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Second timeout test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,0,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (1137934,'cs.LG',1,0);

INSERT INTO arXiv_submission_category_proposal
( proposal_id, submission_id, category, is_primary, proposal_status, user_id, updated, proposal_comment_id, response_comment_id)
values(      1,       1137934, 'hep-ph' ,          0,               0,   20584, '2021-06-02 13:27:49',            21317484,                NULL);

-- a cross submission
-- it's a little fake because it doens't have a paper with it
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(3400,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-16 19:58:40','2015-11-17 14:15:41', 1, NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'Second timeout test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Second timeout test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'cross',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,0,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES
(3400,'cs.LG',1,1),
(3400,'cs.DD',0,1),
(3400,'hep-ph',0,0);


-- a replacement submission
-- it's a little fake because it doens't have a paper with it
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(3401,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-16 19:58:40','2015-11-17 14:15:41', 1, NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'Second timeout test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Second timeout test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'rep',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,0,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES
(3401,'hep-ph',1,1),
(3401,'hep-ex',0,1);


--- a submission with proposals
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(4400,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-16 19:58:40','2015-11-17 14:15:41', 1, NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'proposal test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Proposal test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,0,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES
(4400,'cs.LG',1,1),
(4400,'cs.DD',0,1),
(4400,'hep-ph',0,0);

--- a cross submission
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(4401,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-16 19:58:40','2015-11-17 14:15:41', 1, NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'proposal test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Proposal test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'cross',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,0,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES
(4401,'cs.LG',1,1),
(4401,'cs.DD',0,1),
(4401,'hep-ph',0,0);

--- a cross submission with more than one category
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(4402,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-17 19:58:40','2015-11-18 14:15:41', 1, NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'proposal test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Proposal test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'cross',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,0,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES
(4402,'cs.LG',1,1),
(4402,'cs.DD',0,1),
(4402,'hep-ph',0,0),
(4402,'cs.AI',0,0);

--- a new submission with more than one category
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(4403,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-17 19:58:40','2015-11-18 14:15:41', 1, NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'proposal test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Proposal test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,0,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES
(4403,'cs.LG',1,0),
(4403,'cs.DD',0,0),
(4403,'hep-ph',0,0),
(4403,'cs.AI',0,0);

--- a new submission on auto_hold (Legacy style hold with auto_hold set)
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(441708,NULL,NULL,NULL,1,1,1,1,5,246231,'Brandon Barker','beb82@cornell.edu','2015-11-17 19:58:40','2015-11-18 14:15:41', 2, NULL,0,NULL,NULL,1502662,'pdftex','',0,0,'proposal test case','Brandon barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Proposal test case','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',0,0,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/extraction_timeout1_1137932.tar.gz',NULL,1,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES
(441708,'q-bio.CB',1,0);

--- a submission with bad classifier JSON
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(1234888,NULL,NULL,NULL,1,1,1,1,4 /* stage */,246231,'Brandon Barker','beb82@cornell.edu','2015-10-12 17:11:21','2015-10-12 21:58:44',1 /* status */,NULL,0,'2015-11-17 15:11:21',NULL,2848951,'pdf','1',0,0,'MPI 3 One more time','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'The Message Passing Interface, version three point zero.','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',NULL,NULL,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/Kubla_Khan.pdf',NULL,0,NULL);

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (1234888,'q-bio.CB',1,0);


INSERT INTO `arXiv_submission_abs_classifier_data`
( `submission_id`, `json`, `last_update`, `status`, `message`,
`is_oversize`, `suggested_primary`, `suggested_reason`,
`autoproposal_primary`, `autoproposal_reason`,
`classifier_service_version`, `classifier_model_version`)
VALUES(
1234888,
'total-junk-json',
'2021-04-13 12:49:38', 'success', NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL);

--- a submission in status "working"
INSERT INTO `arXiv_submissions`
(`submission_id`, `document_id`, `doc_paper_id`, `sword_id`, `userinfo`, `is_author`, `agree_policy`, `viewed`, `stage`, `submitter_id`, `submitter_name`, `submitter_email`, `created`, `updated`, `status`, `sticky_status`, `must_process`, `submit_time`, `release_time`, `source_size`, `source_format`, `source_flags`, `has_pilot_data`, `is_withdrawn`, `title`, `authors`, `comments`, `proxy`, `report_num`, `msc_class`, `acm_class`, `journal_ref`, `doi`, `abstract`, `license`, `version`, `type`, `is_ok`, `admin_ok`, `allow_tex_produced`, `remote_addr`, `remote_host`, `package`, `rt_ticket_id`, `auto_hold`, `is_oversize`)
VALUES
(888,NULL,NULL,NULL,1,1,1,1,4 /* stage */,246231,'Brandon Barker','beb82@cornell.edu','2015-10-12 17:11:21','2015-10-12 21:58:44',0 /* status */,NULL,0,'2015-11-17 15:11:21',NULL,2848951,'pdf','1',0,0,'MPI 3 One more time','Brandon Barker',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'The Message Passing Interface, version three point zero.','http://arxiv.org/licenses/nonexclusive-distrib/1.0/',1,'new',NULL,NULL,0,'128.84.31.207','bbsurfacepro3.tc.cornell.edu','/users/e-prints/arXivLib/t/user_data/Kubla_Khan.pdf',NULL,0,NULL);

--- a submission in status "published"

INSERT INTO `arXiv_submissions`
(`submission_id`,`document_id`,`doc_paper_id`,`sword_id`,`userinfo`,`is_author`,`agree_policy`,`viewed`,`stage`,`submitter_id`,`submitter_name`,`submitter_email`,`created`,`updated`,`status`,`sticky_status`,`must_process`,`submit_time`,`release_time`,`source_size`,`source_format`,`source_flags`,`has_pilot_data`,`is_withdrawn`,`title`,`authors`,`comments`,`proxy`,`report_num`,`msc_class`,`acm_class`,`journal_ref`,`doi`,`abstract`,`license`,`version`,`type`,`is_ok`,`admin_ok`,`allow_tex_produced`,`is_oversize`,`remote_addr`,`remote_host`,`package`,`rt_ticket_id`,`auto_hold`,`is_locked`)
VALUES
(4024428 , NULL , NULL   , NULL , 1 , 1 , 1 , 1 , 5 , 246231 ,'xyz','x@x.com','2021-11-12 05:43:20','2021-11-22 01:22:33', 7 , NULL , 0 ,'2021-11-19 01:42:49', NULL         , 2893811 ,'pdf', 1            , 0 , 0 ,'Aqueous Alteration on Asteroids Simplifies Soluble Organic Matter Mixtures','Junko Isa, Fran\c{c}ois-r\''egis Orthous-Daunay, Pierre Beck, Christopher D. K. Herd, Veronique Vuitton, and Laur\`ene Flandinet','29 pages', NULL  , NULL       , NULL      , NULL      ,'ApJL 920 L39 (2021)','10.3847/2041-8213/ac2b34','Biologically relevant abiotic extraterrestrial soluble organic matter (SOM) has been widely investigated to study the origin of life and the chemical evolution of protoplanetary disks. Synthesis of biologically relevant organics, in particular, seems to require aqueous environments in the early solar system.','http://creativecommons.org/licenses/by/4.0/', 1 ,'new', 1 , 0 , 0 , NULL ,'127.0.0.1','xyz.ac.jp','/data/new/4024/4024428/4024428.pdf', NULL , 0 , 0  );

INSERT INTO `arXiv_submission_category`
(`submission_id`, `category`, `is_primary`, `is_published`)
VALUES (4024428,'astro-ph.EP',1,1), (4024428,'physics.data-an',0,1);

INSERT INTO tapir_users VALUES
(29538, 'Michael J.','ODonnell', '', 1, 1, 'michael_odonnell@acm.org', 8, 0, 3, 942856736, NULL, 'satisfaction.cs.uchicago.edu', 0, 0, 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(41106, 'Thomas','Dietterich', '', 1, 1, 'tgd@cs.orst.edu', 8, 0, 3, 927294463, NULL, 'thomas.iiia.csic.es', 0, 0, 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(197598, 'Paolo','Bientinesi', '', 1, 1, 'pauldj@cs.umu.se', 8, 0, 2, 1332970719, '178.202.74.4', 'ip-178-202-74-4.unitymediagroup.de', 0, 0, 0, 1, 1, 0, 0, 0, 0, 'ip-109-91-184-240.unitymediagroup.de.1319607367671678', 0, 0),
(399388, 'Sharon','Gannot', '', 1, 1, 'sharon.gannot@biu.ac.il', 8, 0, 2, 1503689312, '109.64.53.231', 'bzq-109-64-53-231.red.bezeqint.net', 0, 0, 0, 1, 1, 0, 0, 0, 0, '', 0, 0),
(505770, 'Julien','Corman', '', 1, 1, 'corman@inf.unibz.it', 8, 0, 2, 1555515974, '46.18.27.5', 'nat5.unibz.it', 0, 0, 0, 1, 1, 0, 0, 0, 0, '46.18.27.5.1555510862794081', 0, 0);


INSERT INTO tapir_nicknames VALUES
(   29536 , 'odonnell'     ,   29538 ,        1 ,          1 ,    0 ,      0 ,            1 ),
(   41104 , 'tgd'          ,   41106 ,        1 ,          1 ,    0 ,      0 ,            1 ),
(  197582 , 'pauldj'       ,  197598 ,        1 ,          1 ,    0 ,      0 ,            1 ),
(  399358 , 'gannotsh'     ,  399388 ,        1 ,          1 ,    0 ,      0 ,            1 ),
(  503275 , 'juliencorman' ,  505770 ,        1 ,          1 ,    0 ,      0 ,            1 );


INSERT INTO arXiv_admin_log VALUES
( 20783162, NULL, '2021-04-11 23:54:50', NULL, 'system', NULL, 'Submission','admin comment', 'Auto Proposed: cs.LG as primary: selected primary cs.AI not found in classifier scores', NULL, 4400, 0 ),
( 21417006, NULL, '2021-06-10 17:37:13', 'submit/4400', 'juliencorman', '151.62.123.212', 'Admin::Queue','admin comment', 'Proposed: eess.AS as primary: per classifier', 0, 4400, 1 ),
( 21417007, NULL, '2021-06-10 17:37:13', 'submit/4400', 'juliencorman', '151.62.123.212', 'Admin::Queue','admin comment', 'Proposed: eess.AS as primary: per classifier', 0, 4400, 1 ),
( 21417008, NULL, '2021-06-10 17:37:05', 'submit/4400', 'juliencorman', '151.62.123.212', 'Admin::Queue','admin comment', 'Rejected category cs.AI as primary and put on Hold; cs.AI => none', 0, 4400, 1 ),
( 21468534, NULL, '2021-06-15 23:54:41', 'submit/4400', 'tgd', 'c-73-240-154-85.hsd1.or.comcast.net', 'Admin::Queue','admin comment', 'Proposal response: accepted cs.LG as primary', 0, 4400, 1 ),
( 21468535, NULL, '2021-06-15 23:54:45', 'submit/4400', 'tgd', 'c-73-240-154-85.hsd1.or.comcast.net', 'Admin::Queue','admin comment', 'Proposed: cs.SD as secondary', 0, 4400, 1 ),
( 21468573, NULL, '2021-06-16 00:13:35', 'submit/4400', 'odonnell', '97-121-180-117.clsp.qwest.net', 'Admin::Queue','admin comment', 'Proposal response: accepted cs.SD as secondary', 0, 4400, 1 ),
( 21478999, NULL, '2021-06-16 16:42:53', 'submit/4400', 'gannotsh', '5.29.20.105', 'Admin::Queue','admin comment', 'Proposal response: accepted eess.AS as primary', 0, 4400, 1 ),
( 21511145, NULL, '2021-06-20 02:55:12', 'submit/4400', 'pauldj', '217-215-91-53-no600.tbcn.telia.com', 'Admin::Queue','admin comment', 'Rejected category cs.CE as primary and put on Hold; cs.CE cs.LG cs.SD => no primary cs.LG cs.SD: This has no relevance to cs.CE', 0, 4400, 1 );


INSERT INTO  arXiv_submission_category_proposal VALUES
(      203909 ,       4400 , 'cs.LG'    ,          1 ,               1 ,   41106 , '2021-06-16 03:54:41' ,            20783162 ,            21468534 ),
(      214186 ,       4400 , 'eess.AS'  ,          1 ,               1 ,  399388 , '2021-06-16 20:42:53' ,            21417006 ,            21478999 ),
(      214187 ,       4400 , 'eess.AS'  ,          1 ,               0 ,  505770 , '2021-06-10 21:37:13' ,            21417007 ,                NULL ),
(      214188 ,       4400 , 'cs.AI'    ,          1 ,               3 ,  505770 , '2021-06-10 21:37:05' ,            21417008 ,                NULL ),
(      214995 ,       4400 , 'cs.SD'    ,          0 ,               2 ,   29538 , '2021-06-16 04:13:35' ,            21468535 ,            21468573 ),
(      215605 ,       4400 , 'cs.CE'    ,          1 ,               3 ,  197598 , '2021-06-20 06:55:12' ,            21511145 ,                NULL );

-- LOCK TABLES `arXiv_categories` WRITE;

INSERT INTO `arXiv_categories` VALUES ('acc-phys','',1,0,'Accelerator Physics','d','d',0,'acc-phys'),('adap-org','',1,0,'Adaptation, Noise, and Self-Organizing Systems','d','d',0,'adap-org'),('alg-geom','',1,0,'Algebraic Geometry','d','d',0,'alg-geom'),('ao-sci','',1,0,'Atmospheric-Oceanic Sciences','d','d',0,'ao-sci'),('astro-ph','',1,1,'Astrophysics','d','d',0,'astro-ph'),('astro-ph','CO',1,1,'Cosmology and Nongalactic Astrophysics','d','d',0,'astro-ph'),('astro-ph','EP',1,1,'Earth and Planetary Astrophysics','d','d',0,'astro-ph'),('astro-ph','GA',1,1,'Astrophysics of Galaxies','d','d',0,'astro-ph'),('astro-ph','HE',1,1,'High Energy Astrophysical Phenomena','d','d',0,'astro-ph'),('astro-ph','IM',1,1,'Instrumentation and Methods for Astrophysics','d','d',0,'astro-ph'),('astro-ph','SR',1,1,'Solar and Stellar Astrophysics','d','d',0,'astro-ph'),('atom-ph','',1,0,'Atomic, Molecular and Optical Physics','d','d',0,'atom-ph'),('bayes-an','',1,0,'Bayesian Analysis','d','d',0,'bayes-an'),('chao-dyn','',1,0,'Chaotic Dynamics','d','d',0,'chao-dyn'),('chem-ph','',1,0,'Chemical Physics','d','d',0,'chem-ph'),('cmp-lg','',1,0,'Computation and Language','d','d',0,'cmp-lg'),('comp-gas','',1,0,'Cellular Automata and Lattice Gases','d','d',0,'comp-gas'),('cond-mat','',0,1,'Condensed Matter','d','d',0,'cond-mat'),('cond-mat','dis-nn',1,1,'Disordered Systems and Neural Networks','d','d',0,'cond-mat'),('cond-mat','mes-hall',1,1,'Mesoscale and Nanoscale Physics','d','d',0,'cond-mat'),('cond-mat','mtrl-sci',1,1,'Materials Science','d','d',0,'cond-mat'),('cond-mat','none',1,0,'Condensed Matter','d','d',0,'cond-mat'),('cond-mat','other',1,1,'Other Condensed Matter','d','d',0,'cond-mat'),('cond-mat','quant-gas',1,1,'Quantum Gases','d','d',0,'cond-mat'),('cond-mat','soft',1,1,'Soft Condensed Matter','d','d',0,'cond-mat'),('cond-mat','stat-mech',1,1,'Statistical Mechanics','d','d',0,'cond-mat'),('cond-mat','str-el',1,1,'Strongly Correlated Electrons','d','d',0,'cond-mat'),('cond-mat','supr-con',1,1,'Superconductivity','d','d',0,'cond-mat'),('cs','',0,1,'Computer Science','d','d',0,'cs'),('cs','AI',1,1,'Artificial Intelligence','d','d',0,'cs'),('cs','AR',1,1,'Hardware Architecture','d','d',0,'cs'),('cs','CC',1,1,'Computational Complexity','d','d',0,'cs'),('cs','CE',1,1,'Computational Engineering, Finance, and Science','d','d',0,'cs'),('cs','CG',1,1,'Computational Geometry','d','d',0,'cs'),('cs','CL',1,1,'Computation and Language','d','d',0,'cs'),('cs','CR',1,1,'Cryptography and Security','d','d',0,'cs'),('cs','CV',1,1,'Computer Vision and Pattern Recognition','d','d',0,'cs'),('cs','CY',1,1,'Computers and Society','d','d',0,'cs'),('cs','DB',1,1,'Databases','d','d',0,'cs'),('cs','DC',1,1,'Distributed, Parallel, and Cluster Computing','d','d',0,'cs'),('cs','DL',1,1,'Digital Libraries','d','d',0,'cs'),('cs','DM',1,1,'Discrete Mathematics','d','d',0,'cs'),('cs','DS',1,1,'Data Structures and Algorithms','d','d',0,'cs'),('cs','ET',1,1,'Emerging Technologies','d','d',0,'cs'),('cs','FL',1,1,'Formal Languages and Automata Theory','d','d',0,'cs'),('cs','GL',1,1,'General Literature','d','d',0,'cs'),('cs','GR',1,1,'Graphics','d','d',0,'cs'),('cs','GT',1,1,'Computer Science and Game Theory','d','d',0,'cs'),('cs','HC',1,1,'Human-Computer Interaction','d','d',0,'cs'),('cs','IR',1,1,'Information Retrieval','d','d',0,'cs'),('cs','IT',1,1,'Information Theory','d','d',0,'cs'),('cs','LG',1,1,'Learning','d','d',0,'cs'),('cs','LO',1,1,'Logic in Computer Science','d','d',0,'cs'),('cs','MA',1,1,'Multiagent Systems','d','d',0,'cs'),('cs','MM',1,1,'Multimedia','d','d',0,'cs'),('cs','MS',1,1,'Mathematical Software','d','d',0,'cs'),('cs','NA',1,1,'Numerical Analysis','d','d',0,'cs'),('cs','NE',1,1,'Neural and Evolutionary Computing','d','d',0,'cs'),('cs','NI',1,1,'Networking and Internet Architecture','d','d',0,'cs'),('cs','OH',1,1,'Other Computer Science','d','d',0,'cs'),('cs','OS',1,1,'Operating Systems','d','d',0,'cs'),('cs','PF',1,1,'Performance','d','d',0,'cs'),('cs','PL',1,1,'Programming Languages','d','d',0,'cs'),('cs','RO',1,1,'Robotics','d','d',0,'cs'),('cs','SC',1,1,'Symbolic Computation','d','d',0,'cs'),('cs','SD',1,1,'Sound','d','d',0,'cs'),('cs','SE',1,1,'Software Engineering','d','d',0,'cs'),('cs','SI',1,1,'Social and Information Networks','d','d',0,'cs'),('cs','SY',1,1,'Systems and Control','d','d',0,'cs'),('dg-ga','',1,0,'Differential Geometry','d','d',0,'dg-ga'),('econ','',0,1,'Economics','d','d',0,'econ'),('econ','EM',1,1,'Econometrics','d','d',0,'econ'),('econ','GN',1,1,'General Economics','d','d',0,'econ'),('econ','TH',1,1,'Theoretical Economics','d','d',0,'econ'),('eess','',0,1,'Electrical Engineering and Systems Science','d','d',0,'eess'),('eess','AS',1,1,'Audio and Speech Processing','d','d',0,'eess'),('eess','IV',1,1,'Image and Video Processing','d','d',0,'eess'),('eess','SP',1,1,'Signal Processing','d','d',0,'eess'),('eess','SY',1,1,'Systems and Control','d','d',0,'eess'),('funct-an','',1,0,'Functional Analysis','d','d',0,'funct-an'),('gr-qc','',1,1,'General Relativity and Quantum Cosmology','d','d',0,'gr-qc'),('hep-ex','',1,1,'High Energy Physics - Experiment','d','d',0,'hep-ex'),('hep-lat','',1,1,'High Energy Physics - Lattice','d','d',0,'hep-lat'),('hep-ph','',1,1,'High Energy Physics - Phenomenology','d','d',0,'hep-ph'),('hep-th','',1,1,'High Energy Physics - Theory','d','d',0,'hep-th'),('math','',0,1,'Mathematics','d','d',0,'math'),('math','AC',1,1,'Commutative Algebra','d','d',0,'math'),('math','AG',1,1,'Algebraic Geometry','d','d',0,'math'),('math','AP',1,1,'Analysis of PDEs','d','d',0,'math'),('math','AT',1,1,'Algebraic Topology','d','d',0,'math'),('math','CA',1,1,'Classical Analysis and ODEs','d','d',0,'math'),('math','CO',1,1,'Combinatorics','d','d',0,'math'),('math','CT',1,1,'Category Theory','d','d',0,'math'),('math','CV',1,1,'Complex Variables','d','d',0,'math'),('math','DG',1,1,'Differential Geometry','d','d',0,'math'),('math','DS',1,1,'Dynamical Systems','d','d',0,'math'),('math','FA',1,1,'Functional Analysis','d','d',0,'math'),('math','GM',1,1,'General Mathematics','d','d',0,'math.GM'),('math','GN',1,1,'General Topology','d','d',0,'math'),('math','GR',1,1,'Group Theory','d','d',0,'math'),('math','GT',1,1,'Geometric Topology','d','d',0,'math'),('math','HO',1,1,'History and Overview','d','d',0,'math'),('math','IT',1,1,'Information Theory','d','d',0,'math'),('math','KT',1,1,'K-Theory and Homology','d','d',0,'math'),('math','LO',1,1,'Logic','d','d',0,'math'),('math','MG',1,1,'Metric Geometry','d','d',0,'math'),('math','MP',1,1,'Mathematical Physics','d','d',0,'math'),('math','NA',1,1,'Numerical Analysis','d','d',0,'math'),('math','NT',1,1,'Number Theory','d','d',0,'math'),('math','OA',1,1,'Operator Algebras','d','d',0,'math'),('math','OC',1,1,'Optimization and Control','d','d',0,'math'),('math','PR',1,1,'Probability','d','d',0,'math'),('math','QA',1,1,'Quantum Algebra','d','d',0,'math'),('math','RA',1,1,'Rings and Algebras','d','d',0,'math'),('math','RT',1,1,'Representation Theory','d','d',0,'math'),('math','SG',1,1,'Symplectic Geometry','d','d',0,'math'),('math','SP',1,1,'Spectral Theory','d','d',0,'math'),('math','ST',1,1,'Statistics Theory','d','d',0,'math'),('math-ph','',1,1,'Mathematical Physics','d','d',0,'math-ph'),('mtrl-th','',1,0,'Materials Theory','d','d',0,'mtrl-th'),('nlin','',0,1,'Nonlinear Sciences','d','d',0,'nlin'),('nlin','AO',1,1,'Adaptation and Self-Organizing Systems','d','d',0,'nlin'),('nlin','CD',1,1,'Chaotic Dynamics','d','d',0,'nlin'),('nlin','CG',1,1,'Cellular Automata and Lattice Gases','d','d',0,'nlin'),('nlin','PS',1,1,'Pattern Formation and Solitons','d','d',0,'nlin'),('nlin','SI',1,1,'Exactly Solvable and Integrable Systems','d','d',0,'nlin'),('nucl-ex','',1,1,'Nuclear Experiment','d','d',0,'nucl-ex'),('nucl-th','',1,1,'Nuclear Theory','d','d',0,'nucl-th'),('patt-sol','',1,0,'Pattern Formation and Solitons','d','d',0,'patt-sol'),('physics','',0,1,'Physics','d','d',0,'physics'),('physics','acc-ph',1,1,'Accelerator Physics','d','d',0,'physics.acc-ph'),('physics','ao-ph',1,1,'Atmospheric and Oceanic Physics','d','d',0,'physics.ao-ph'),('physics','app-ph',1,1,'Applied Physics','d','d',0,'physics'),('physics','atm-clus',1,1,'Atomic and Molecular Clusters','d','d',0,'physics.atm-clus'),('physics','atom-ph',1,1,'Atomic Physics','d','d',0,'physics.atom-ph'),('physics','bio-ph',1,1,'Biological Physics','d','d',0,'physics.bio-ph'),('physics','chem-ph',1,1,'Chemical Physics','d','d',0,'physics.chem-ph'),('physics','class-ph',1,1,'Classical Physics','d','d',0,'physics.class-ph'),('physics','comp-ph',1,1,'Computational Physics','d','d',0,'physics.comp-ph'),('physics','data-an',1,1,'Data Analysis, Statistics and Probability','d','d',0,'physics.data-an'),('physics','ed-ph',1,1,'Physics Education','d','d',0,'physics.ed-ph'),('physics','flu-dyn',1,1,'Fluid Dynamics','d','d',0,'physics.flu-dyn'),('physics','gen-ph',1,1,'General Physics','d','d',0,'physics.gen-ph'),('physics','geo-ph',1,1,'Geophysics','d','d',0,'physics.geo-ph'),('physics','hist-ph',1,1,'History and Philosophy of Physics','d','d',0,'physics.hist-ph'),('physics','ins-det',1,1,'Instrumentation and Detectors','d','d',0,'physics.ins-det'),('physics','med-ph',1,1,'Medical Physics','d','d',0,'physics.med-ph'),('physics','optics',1,1,'Optics','d','d',0,'physics.optics'),('physics','plasm-ph',1,1,'Plasma Physics','d','d',0,'physics.plasm-ph'),('physics','pop-ph',1,1,'Popular Physics','d','d',0,'physics.pop-ph'),('physics','soc-ph',1,1,'Physics and Society','d','d',0,'physics.soc-ph'),('physics','space-ph',1,1,'Space Physics','d','d',0,'physics.space-ph'),('plasm-ph','',1,0,'Plasma Physics','d','d',0,'plasm-ph'),('q-alg','',1,0,'Quantum Algebra and Topology','d','d',0,'q-alg'),('q-bio','',0,1,'Quantitative Biology','d','d',0,'q-bio'),('q-bio','BM',1,1,'Biomolecules','d','d',0,'q-bio'),('q-bio','CB',1,1,'Cell Behavior','d','d',0,'q-bio'),('q-bio','GN',1,1,'Genomics','d','d',0,'q-bio'),('q-bio','MN',1,1,'Molecular Networks','d','d',0,'q-bio'),('q-bio','NC',1,1,'Neurons and Cognition','d','d',0,'q-bio'),('q-bio','OT',1,1,'Other Quantitative Biology','d','d',0,'q-bio'),('q-bio','PE',1,1,'Populations and Evolution','d','d',0,'q-bio'),('q-bio','QM',1,1,'Quantitative Methods','d','d',0,'q-bio'),('q-bio','SC',1,1,'Subcellular Processes','d','d',0,'q-bio'),('q-bio','TO',1,1,'Tissues and Organs','d','d',0,'q-bio'),('q-fin','',0,1,'Quantitative Finance','d','d',0,'q-fin'),('q-fin','CP',1,1,'Computational Finance','d','d',0,'q-fin'),('q-fin','EC',1,1,'Economics','d','d',0,'q-fin'),('q-fin','GN',1,1,'General Finance','d','d',0,'q-fin'),('q-fin','MF',1,1,'Mathematical Finance','d','d',0,'q-fin'),('q-fin','PM',1,1,'Portfolio Management','d','d',0,'q-fin'),('q-fin','PR',1,1,'Pricing of Securities','d','d',0,'q-fin'),('q-fin','RM',1,1,'Risk Management','d','d',0,'q-fin'),('q-fin','ST',1,1,'Statistical Finance','d','d',0,'q-fin'),('q-fin','TR',1,1,'Trading and Market Microstructure','d','d',0,'q-fin'),('quant-ph','',1,1,'Quantum Physics','d','d',0,'quant-ph'),('solv-int','',1,0,'Exactly Solvable and Integrable Systems','d','d',0,'solv-int'),('stat','',0,1,'Statistics','d','d',0,'stat'),('stat','AP',1,1,'Applications','d','d',0,'stat'),('stat','CO',1,1,'Computation','d','d',0,'stat'),('stat','ME',1,1,'Methodology','d','d',0,'stat'),('stat','ML',1,1,'Machine Learning','d','d',0,'stat'),('stat','OT',1,1,'Other Statistics','d','d',0,'stat'),('stat','TH',1,1,'Statistics Theory','d','d',0,'stat'),('supr-con','',1,0,'Superconductivity','d','d',0,'supr-con'),('test','',0,1,'Test','d','d',0,'test'),('test','dis-nn',1,1,'Test Disruptive Networks','d','d',0,'test'),('test','mes-hall',1,1,'Test Hall','d','d',0,'test'),('test','mtrl-sci',1,1,'Test Mtrl-Sci','d','d',0,'test'),('test','none',1,1,'','d','d',0,'test'),('test','soft',1,1,'Test Soft','d','d',0,'test'),('test','stat-mech',1,1,'Test Mechanics','d','d',0,'test'),('test','str-el',1,1,'Test Electrons','d','d',0,'test'),('test','supr-con',1,1,'Test Superconductivity','d','d',0,'test');

-- UNLOCK TABLES;

-- LOCK TABLES `arXiv_archives` WRITE;

INSERT INTO `arXiv_archives` VALUES ('acc-phys','physics','Accelerator Physics','9411','9609',0),('adap-org','physics','Adaptation, Noise, and Self-Organizing Systems','9303','9912',0),('alg-geom','math','Algebraic Geometry','9202','9712',0),('ao-sci','physics','Atmospheric-Oceanic Sciences','9502','9609',0),('astro-ph','physics','Astrophysics','9204','',0),('atom-ph','physics','Atomic, Molecular and Optical Physics','9509','9609',0),('bayes-an','physics','Bayesian Analysis','9506','9611',0),('chao-dyn','physics','Chaotic Dynamics','9301','9912',0),('chem-ph','physics','Chemical Physics','9403','9609',0),('cmp-lg','cs','Computation and Language','9404','9809',0),('comp-gas','physics','Cellular Automata and Lattice Gases','9302','9912',0),('cond-mat','physics','Condensed Matter','9204','',1),('cs','cs','Computer Science','9301','',2),('dg-ga','math','Differential Geometry','9406','9712',0),('econ','econ','Economics','1709','',2),('eess','eess','Electrical Engineering and Systems Science','1709','',2),('funct-an','math','Functional Analysis','9204','9712',0),('gr-qc','physics','General Relativity and Quantum Cosmology','9207','',0),('hep-ex','physics','High Energy Physics - Experiment','9404','',0),('hep-lat','physics','High Energy Physics - Lattice','9202','',0),('hep-ph','physics','High Energy Physics - Phenomenology','9203','',0),('hep-th','physics','High Energy Physics - Theory','9108','',0),('math','math','Mathematics','9202','',2),('math-ph','physics','Mathematical Physics','9609','',0),('mtrl-th','physics','Materials Theory','9411','9609',0),('nlin','physics','Nonlinear Sciences','9301','',2),('nucl-ex','physics','Nuclear Experiment','9412','',0),('nucl-th','physics','Nuclear Theory','9210','',0),('patt-sol','physics','Pattern Formation and Solitons','9302','9912',0),('physics','physics','Physics','9610','',2),('plasm-ph','physics','Plasma Physics','9509','9609',0),('q-alg','math','Quantum Algebra and Topology','9412','9712',0),('q-bio','q-bio','Quantitative Biology','0309','',2),('q-fin','q-fin','Quantitative Finance','0812','',2),('quant-ph','physics','Quantum Physics','9412','',0),('solv-int','physics','Exactly Solvable and Integrable Systems','9304','9912',0),('stat','stat','Statistics','0704','',2),('supr-con','physics','Superconductivity','9411','9609',0),('test','test','Test','9502','',1);

-- UNLOCK TABLES;

-- LOCK TABLES `arXiv_endorsement_domains` WRITE;

INSERT INTO `arXiv_endorsement_domains` VALUES ('acc-phys','n','n','y',4),('adap-org','n','n','y',4),('alg-geom','n','n','y',4),('ao-sci','n','n','y',4),('astro-ph','n','n','y',4),('atom-ph','n','n','y',4),('bayes-an','n','n','y',4),('chao-dyn','n','n','y',4),('chem-ph','n','n','y',4),('cmp-lg','n','n','y',4),('comp-gas','n','n','y',4),('cond-mat','n','n','y',4),('cs','n','y','y',3),('dg-ga','n','n','y',4),('econ','n','y','y',3),('eess','n','y','y',3),('funct-an','n','n','y',4),('gr-qc','n','n','y',4),('hep-ex','n','n','y',4),('hep-lat','n','n','y',4),('hep-ph','n','n','y',4),('hep-th','n','n','y',4),('math','n','n','y',4),('math-ph','n','n','y',4),('math.GM','n','n','y',2),('mtrl-th','n','n','y',4),('nlin','n','n','y',4),('nucl-ex','n','n','y',4),('nucl-th','n','n','y',4),('patt-sol','n','n','y',4),('phys-lib','n','n','y',4),('physics','n','n','y',4),('physics.acc-ph','n','n','y',2),('physics.ao-ph','n','n','y',2),('physics.atm-clus','n','n','y',2),('physics.atom-ph','n','n','y',2),('physics.bio-ph','n','n','y',2),('physics.chem-ph','n','n','y',2),('physics.class-ph','n','n','y',2),('physics.comp-ph','n','n','y',2),('physics.data-an','n','n','y',2),('physics.ed-ph','n','n','y',2),('physics.flu-dyn','n','n','y',2),('physics.gen-ph','n','n','y',2),('physics.geo-ph','n','n','y',2),('physics.hist-ph','n','n','y',2),('physics.ins-det','n','n','y',2),('physics.med-ph','n','n','y',2),('physics.optics','n','n','y',2),('physics.plasm-ph','n','n','y',2),('physics.pop-ph','n','n','y',2),('physics.soc-ph','n','n','y',2),('physics.space-ph','n','n','y',2),('plasm-ph','n','n','y',4),('q-alg','n','n','y',4),('q-bio','n','n','y',2),('q-fin','n','y','y',2),('quant-ph','n','n','y',4),('solv-int','n','n','y',4),('stat','n','n','y',2),('supr-con','n','n','y',4),('test','n','n','y',4);

-- UNLOCK TABLES;


-- LOCK TABLES `arXiv_groups` WRITE;

INSERT INTO `arXiv_groups` VALUES ('cs','Computer Science','1993'),('econ','Economics','2017'),('eess','Electrical Engineering and Systems Science','2017'),('math','Mathematics','1992'),('physics','Physics','1991'),('q-bio','Quantitative Biology','1992'),('q-fin','Quantitative Finance','1997'),('stat','Statistics','1999'),('test','Test','1995');

-- UNLOCK TABLES;
