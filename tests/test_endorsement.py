from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from flask import url_for
import pytest

from arxiv_db.models import Endorsements, EndorsementRequests, Demographics, TapirUsers


@pytest.fixture(scope='session')
def fake_endorsements(db):
     with Session(db) as session:
         endorser = TapirUsers(first_name='Sally', last_name='LongCareer', policy_class=2, email='slc234@cornell.edu')
         session.add(endorser)
         endorsee = TapirUsers(first_name='Aspen', last_name='Early', policy_class=2, email='ase12@cornell.edu')
         session.add(endorsee)
         endorsee_sus = TapirUsers(first_name='Bobby', last_name='NoPapers', policy_class=2, email='bob@scamy.example.com')
         endorsee_sus.demographics = Demographics(flag_suspect=1, archive='cs', subject_class='CR')
         session.add(endorsee_sus)

         req1 = EndorsementRequests(endorsee=endorsee,
                                    secret='end_sec_0',
                                    archive='cs', subject_class='CR',
                                    issued_when=datetime.now(),
                                    flag_valid=1, point_value=10)
         req1.endorsement = Endorsements(endorser=endorser, endorsee=endorsee,                                     archive='cs', subject_class='CR',)

         req2 = EndorsementRequests(endorsee=endorsee_sus,
                                    secret='end_sec_1',
                                    archive='cs', subject_class='CR',
                                    issued_when=datetime.now(),
                                    flag_valid=1, point_value=10)
         req2.endorsement = Endorsements(endorser=endorser,                   endorsee=endorsee_sus    ,              archive='cs', subject_class='CR',)

         req3 = EndorsementRequests(endorsee=endorsee,
                                    secret='end_sec_2',
                                    archive='cs', subject_class='CV',
                                    issued_when=datetime.now(),
                                    flag_valid=1, point_value=-10)
         req3.endorsement = Endorsements(endorser=endorser, endorsee=endorsee         ,                            archive='cs', subject_class='CV')

         req4 = EndorsementRequests(endorsee=endorsee,
                                    secret='end_sec_3',
                                    archive='cs', subject_class='DL',
                                    issued_when=datetime.now() - timedelta(days=4),
                                    flag_valid=1, point_value=10)
         req4.endorsement = Endorsements(endorser=endorser,                  endorsee=endorsee  ,                 archive='cs', subject_class='DL')

         req5 = EndorsementRequests(endorsee=endorsee,
                                    secret='end_sec_5',
                                    archive='cs', subject_class='ET',
                                    issued_when=datetime.now() - timedelta(days=50),
                                    flag_valid=1, point_value=10)
         req5.endorsement = Endorsements(endorser=endorser,                  endorsee=endorsee  ,                 archive='cs', subject_class='ET')

         session.commit()
         def as_html_parts(id):
             return f">{id}</a>";

         return dict(negative=dict(id=req3.request_id,html=as_html_parts(req3.request_id)),
                     older=dict(id=req4.request_id,html=as_html_parts(req4.request_id)),
                     flagged=dict(id=req2.request_id,html=as_html_parts(req2.request_id)),
                     today=dict(id=req1.request_id,html=as_html_parts(req1.request_id)),
                     )


def test_endorsement_reports(admin_client, fake_endorsements):
    resp = admin_client.get(url_for('endorsement.today', flagged=1))
    assert resp.status_code == 200
    txt = resp.data.decode()
    assert fake_endorsements['negative']['html'] not in txt
    assert fake_endorsements['flagged']['html'] in txt
    assert fake_endorsements['today']['html'] not in txt
    assert fake_endorsements['older']['html'] not in txt

    resp = admin_client.get(url_for('endorsement.last_week'))
    assert resp.status_code == 200
    txt = resp.data.decode()
    assert fake_endorsements['negative']['html'] in txt
    assert fake_endorsements['flagged']['html'] in txt
    assert fake_endorsements['today']['html'] in txt
    assert fake_endorsements['older']['html'] in txt

    resp = admin_client.get(url_for('endorsement.negative'))
    assert resp.status_code == 200
    txt = resp.data.decode()
    assert fake_endorsements['negative']['html'] in txt
    assert fake_endorsements['flagged']['html'] not in txt
    assert fake_endorsements['today']['html'] not in txt
    assert fake_endorsements['older']['html'] not in txt

    resp = admin_client.get(url_for('endorsement.today'))
    assert resp.status_code == 200
    txt = resp.data.decode()
    assert fake_endorsements['negative']['html'] in txt
    assert fake_endorsements['flagged']['html'] in txt
    assert fake_endorsements['today']['html'] in txt
    assert fake_endorsements['older']['html'] not in txt

def test_endorsement_detail(admin_client, fake_endorsements):
    resp = admin_client.get(url_for('endorsement.request_detail', endorsement_req_id=0))
    assert resp.status_code == 404

    resp = admin_client.get(url_for('endorsement.request_detail', endorsement_req_id=fake_endorsements['today']['id']))
    assert resp.status_code == 200

    resp = admin_client.get(url_for('endorsement.request_detail', endorsement_req_id=fake_endorsements['flagged']['id']))
    assert resp.status_code == 200

    resp = admin_client.get(url_for('endorsement.request_detail', endorsement_req_id=fake_endorsements['older']['id']))
    assert resp.status_code == 200

    resp = admin_client.get(url_for('endorsement.request_detail', endorsement_req_id=fake_endorsements['negative']['id']))
    assert resp.status_code == 200


def test_bad(admin_client):
    admin_client.get(url_for('endorsement.today', flagged=99)).status_code == 400
    admin_client.get(url_for('endorsement.today', page=1000000)).status_code == 400
    admin_client.get(url_for('endorsement.today', days_back=1000000)).status_code == 400
    admin_client.get(url_for('endorsement.today', per_page=1001)).status_code == 400
