from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from admin_webapp.controllers.ownership import PaperPasswordForm
from flask import url_for
import pytest

from sqlalchemy.exc import IntegrityError

from arxiv_db.models import OwnershipRequests, OwnershipRequestsAudit, Documents, PaperOwners, TapirUsers, PaperPw
from arxiv_db.models.associative_tables import t_arXiv_ownership_requests_papers

from admin_webapp.controllers.ownership import paper_password_post

from werkzeug.datastructures import MultiDict

@pytest.fixture(scope='session')
def fake_ownerships(db):
     with Session(db) as session:
         oreq = OwnershipRequests(
             request_id=1,
             user_id=246231,
             workflow_status='pending')
         session.add(oreq)
         raudit = OwnershipRequestsAudit(
             request_id=1,
             session_id=0,
             remote_addr='127.0.0.1',
             tracking_cookie='127.0.0.1.1999999999999',
             date=datetime.now(),
             )
         session.add(raudit)

         doc = Documents(document_id = 1111, paper_id='2010.01111', title="bogus title",
                         submitter_email="bob@cornell.edu", authors="Smith, Bob",
                         submitter_id=246231, primary_subject_class='cs.IR')
         session.add(doc)

         stmt = insert(t_arXiv_ownership_requests_papers).values(request_id=1, document_id=1111)
         session.execute(stmt)

         oreq = OwnershipRequests(
             request_id=2,
             user_id=246231,
             workflow_status='rejected')
         session.add(oreq)
         raudit = OwnershipRequestsAudit(
             request_id=2,
             session_id=0,
             remote_addr='127.0.0.1',
             tracking_cookie='127.0.0.1.1999999999999',
             date=datetime.now(),
             )
         session.add(raudit)

         doc = Documents(document_id = 2222 , paper_id='2010.02222', title="bogus title",
                         submitter_email="bob@cornell.edu", authors="Smith, Bob",
                         submitter_id=246231, primary_subject_class='cs.IR')
         session.add(doc)

         stmt = insert(t_arXiv_ownership_requests_papers).values(request_id=1, document_id=2222)
         session.execute(stmt)

         oreq = OwnershipRequests(
             request_id=3,
             user_id=246231,
             workflow_status='accepted')
         session.add(oreq)
         raudit = OwnershipRequestsAudit(
             request_id=3,
             session_id=0,
             remote_addr='127.0.0.1',
             tracking_cookie='127.0.0.1.1999999999999',
             date=datetime.now(),
             )
         session.add(raudit)

         doc = Documents(document_id = 3333, paper_id='2010.03333', title="bogus title",
                         submitter_email="bob@cornell.edu", authors="Smith, Bob",
                         submitter_id=246231, primary_subject_class='cs.IR')
         session.add(doc)

         stmt = insert(t_arXiv_ownership_requests_papers).values(request_id=1, document_id=3333)
         session.execute(stmt)

         stmt = session.add(PaperOwners(document_id=3333, user_id=246231, valid=1))

         # need: user/nick/etc request audit, documents, owned_papers,
         session.commit()
         return [1,2,3]

def test_get_reports(admin_client, fake_ownerships):
    resp = admin_client.get(url_for('ownership.pending'))
    assert resp.status_code == 200

    resp = admin_client.get(url_for('ownership.rejected'))
    assert resp.status_code == 200

    resp = admin_client.get(url_for('ownership.accepted'))
    assert resp.status_code == 200

def test_get_detailed_report(admin_client, fake_ownerships):
    resp = admin_client.get(url_for('ownership.display', ownership_id = fake_ownerships[0]))
    assert resp.status_code == 200

    resp = admin_client.get(url_for('ownership.display', ownership_id = fake_ownerships[1]))
    assert resp.status_code == 200

    resp = admin_client.get(url_for('ownership.display', ownership_id = fake_ownerships[2]))
    assert resp.status_code == 200

    resp = admin_client.get(url_for('ownership.display', ownership_id = 0))
    assert resp.status_code == 404

def test_edits(admin_client, fake_ownerships, db):
    with Session(db) as session:
        oreq:OwnershipRequests = session.execute(select(OwnershipRequests)
                                                 .where(OwnershipRequests.user_id==246231,
                                                        OwnershipRequests.workflow_status=='pending')
                                                 ).scalar()
        request_id = oreq.request_id
        assert oreq
        resp = admin_client.post(url_for('ownership.display', ownership_id=oreq.request_id),
                            data = dict(request_id=request_id,
                                        make_owner='make owner',
                                        approve_1111=1,
                                        is_author=1)
                            )
        assert resp.status_code == 200
        session.expire(oreq)
        assert oreq and oreq.workflow_status == 'accepted'

        resp = admin_client.post(url_for('ownership.display', ownership_id=oreq.request_id),
                            data = dict(request_id=request_id,
                                        revisit='revisit',
                                        approve_1111=1,
                                        is_author=1)
                            )
        assert resp.status_code == 200
        session.expire(oreq)
        assert oreq and oreq.workflow_status == 'pending'

        resp = admin_client.post(url_for('ownership.display', ownership_id=oreq.request_id),
                            data = dict(request_id=request_id,
                                        reject='reject',
                                        approve_1111=1,
                                        is_author=1)
                            )
        assert resp.status_code == 200
        session.expire(oreq)
        assert oreq and oreq.workflow_status == 'rejected'


        resp = admin_client.post(url_for('ownership.display', ownership_id=oreq.request_id),
                            data = dict(request_id=request_id,
                                        no_action='no defined submit actions for form')
                            )
        assert resp.status_code == 400

        resp = admin_client.post(url_for('ownership.display', ownership_id=0),
                                 data = dict(request_id=request_id,
                                             make_owner='1')
                                 )
        assert resp.status_code == 404


def test_need_pw_form_controller_success(client, mocker):
     mocked_req = mocker.patch('admin_webapp.controllers.ownership.request', return_value=mocker.MagicMock)
     mocked_doc = mocker.MagicMock()
     mocked_doc.paper_id = '1111.111111'
     mocked_doc.password.password_storage = 0
     mocked_doc.password.password_enc = 'fakepassword'
     mocked_docfn = mocker.patch('admin_webapp.controllers.ownership._get_doc_and_pw', return_value=mocked_doc)
     mocked_add = mocker.patch('admin_webapp.controllers.ownership._add_paper_owner')

     form = PaperPasswordForm()
     form.process(formdata=MultiDict(
          dict(paperid='1111.11111', password='fakepassword', author='Yes', agree=True)))
     data = paper_password_post(form, mocked_req)
     assert data['form'].errors == {}
     assert 'error' not in data
     assert data['success'] == True
     assert mocked_add.called


def test_need_pw_form_controller_invalid(client, mocker):
     mocked_req = mocker.patch('admin_webapp.controllers.ownership.request', return_value=mocker.MagicMock)
     form = PaperPasswordForm()
     form.process(formdata=MultiDict(
          dict(paperid='', password='', author='not_valid_value', agree=True)))
     data = paper_password_post(form, mocked_req)
     assert data['form'].errors != {}
     assert data['error'] == 'FormInvalid'
     assert data['success'] == False


def test_need_pw_form_controller_doc_not_found(client, mocker):
     mocked_req = mocker.patch('admin_webapp.controllers.ownership.request', return_value=mocker.MagicMock)
     mocked_docfn = mocker.patch('admin_webapp.controllers.ownership._get_doc_and_pw', return_value=None)
     form = PaperPasswordForm()
     form.process(formdata=MultiDict(
          dict(paperid='1111.11111', password='client_pw', author='Yes', agree=True)))
     data = paper_password_post(form, mocked_req)
     assert data['success'] == False
     assert data['error'] == 'paperNotFound'

def test_need_pw_form_controller_bad_encoding(client, mocker):
     mocked_req = mocker.patch('admin_webapp.controllers.ownership.request', return_value=mocker.MagicMock)
     mocked_doc = mocker.MagicMock()
     mocked_doc.paper_id = '1111.111111'
     mocked_doc.password.password_storage = 1
     mocked_doc.password.password_enc = 'fakepassword'
     mocked_docfn = mocker.patch('admin_webapp.controllers.ownership._get_doc_and_pw', return_value=mocked_doc)

     form = PaperPasswordForm()
     form.process(formdata=MultiDict(
          dict(paperid='1111.11111', password='fakepassword', author='Yes', agree=True)))
     data = paper_password_post(form, mocked_req)
     assert data['form'].errors == {}
     assert data['success'] == False
     assert data['error'] == 'password encoding must be zero'


def test_need_pw_form_controller_bad_password(client, mocker):
     mocked_req = mocker.patch('admin_webapp.controllers.ownership.request', return_value=mocker.MagicMock)
     mocked_doc = mocker.MagicMock()
     mocked_doc.paper_id = '1111.111111'
     mocked_doc.password.password_storage = 0
     mocked_doc.password.password_enc = 'db_pw'
     mocked_docfn = mocker.patch('admin_webapp.controllers.ownership._get_doc_and_pw', return_value=mocked_doc)

     form = PaperPasswordForm()
     form.process(formdata=MultiDict(
          dict(paperid='1111.11111', password='client_pw', author='Yes', agree=True)))
     data = paper_password_post(form, mocked_req)
     assert data['success'] == False
     assert data['error'] == 'bad password'


def test_need_pw_form_controller_already_owner(client, mocker):
     mocked_req = mocker.patch('admin_webapp.controllers.ownership.request', return_value=mocker.MagicMock)
     mocked_doc = mocker.MagicMock()
     mocked_doc.paper_id = '1111.111111'
     mocked_doc.password.password_storage = 0
     mocked_doc.password.password_enc = 'fakepassword'
     mocked_docfn = mocker.patch('admin_webapp.controllers.ownership._get_doc_and_pw', return_value=mocked_doc)
     mocked_add = mocker.patch('admin_webapp.controllers.ownership._add_paper_owner',
                               side_effect=IntegrityError(statement='fake stmt', params=[], orig='fake orig'))

     form = PaperPasswordForm()
     form.process(formdata=MultiDict(
          dict(paperid='1111.11111', password='fakepassword', author='Yes', agree=True)))
     data = paper_password_post(form, mocked_req)
     assert data['success'] == False
     assert data['error'] == 'already an owner'


def test_add_ownership_via_password(reader_client, db):
     with Session(db) as session:
          doc = Documents(document_id = 444, paper_id='2010.04444', title="bogus title",
                          submitter_email="bob@cornell.edu", authors="Smith, Bob",
                          submitter_id=246231, primary_subject_class='cs.IR')
          doc.password = PaperPw(password_storage=0, password_enc='1234')
          session.add(doc)
          session.commit()

          prexisting_ownership = session.scalar(select(PaperOwners)
                                                .filter(PaperOwners.document_id == 444)
                                                .filter(PaperOwners.user_id == reader_client.user_id))
          assert not prexisting_ownership

          res= reader_client.post(url_for('ownership.need_papper_password'),
                                  data = PaperPasswordForm(paperid='2010.04444',
                                                           password='1234',
                                                           author='Yes',
                                                           agree=True).data)
          assert res.status_code == 200

          new_ownership = session.scalar(select(PaperOwners)
                                         .filter(PaperOwners.document_id == 444)
                                         .filter(PaperOwners.user_id == reader_client.user_id))
          assert new_ownership
