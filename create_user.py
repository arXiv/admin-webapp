"""
Script for creating a new user. For dev/test purposes only.

From arxiv-auth/accounts

.. warning: DO NOT USE THIS ON A PRODUCTION DATABASE.

"""
import typing
from typing import Tuple
from zoneinfo import ZoneInfo

import random
from datetime import datetime
import click

from arxiv.taxonomy import definitions
from arxiv.db import models, transaction
from arxiv.auth.legacy import util, passwords

from admin_webapp.factory import create_web_app
from ruamel.yaml import YAML

EASTERN = ZoneInfo('US/Eastern')

@click.group()
def cli() -> None:
    pass


def _random_category() -> Tuple[str, str]:
    category = random.choice(list(definitions.CATEGORIES.items()))
    archive = category[1].in_archive
    subject_class = category[0].split('.')[-1] if '.' in category[0] else ''
    return archive, subject_class


def _prob(P: int) -> bool:
    return random.randint(0, 100) < P


def create_users(specs: typing.List[dict]):
    app = create_web_app(CREATE_DB=True)
    with app.app_context():
        with transaction() as session:
            for user_data in specs["users"]:
                user = user_data["user"]
                nick = user_data["nick"]
                profile = user_data["profile"]
                pw_spec = user_data["password"]
                db_user = models.TapirUser(**user)
                session.add(db_user)

                # Create a username.
                nick["user"] = db_user
                db_nick = models.TapirNickname(**nick)

                # Create the user's profile.
                profile["user"] = db_user
                db_profile = models.Demographic(**profile)

                # Set the user's password.
                pw_spec["user"] = db_user
                if "password_cleartext" in pw_spec:
                    pw_spec["password_enc"] = passwords.hash_password(pw_spec["password_cleartext"])
                    del pw_spec["password_cleartext"]
                    pass
                if "password_storage" not in pw_spec:
                    pw_spec["password_storage"] = 2

                db_password = models.TapirUsersPassword(**pw_spec)

                session.add(db_password)
                session.add(db_nick)
                session.add(db_profile)

            session.commit()


@cli.command("load-users")
@click.argument('users', type=click.File('r'))
def load_users(users: click.File) -> None:
    """Create users from file"""
    create_users(YAML().load(users))



@cli.command("create-user")
@click.option('--username', prompt='Your username', default='bob')
@click.option('--email', prompt='Your email address', default='bogus@example.com')
@click.option('--password', prompt='Your password')
@click.option('--first-name', prompt='Your first name', default='Bob')
@click.option('--last-name', prompt='Your last name', default='Smith')
@click.option('--suffix-name', prompt='Your name suffix', default='')
@click.option('--affiliation', prompt='Your affiliation', default='FSU')
@click.option('--home-page', prompt='Your homepage', default='https://asdf.com')
def create_user(username: str, email: str, password: str,
                first_name: str, last_name: str, suffix_name: str = '',
                affiliation: str = 'FSU', home_page: str = 'https://asdf.com') -> None:
    """Create a new user. For dev/test purposes only."""
    ip_addr = '127.0.0.1'
    joined_date = util.epoch(datetime.now().replace(tzinfo=EASTERN))
    archive, subject_class = _random_category()
    this = {
        "user": {
            "first_name": first_name,
            "last_name": last_name,
            "suffix_name": suffix_name,
            "share_first_name": 1,
            "share_last_name": 1,
            "email": email,
            "flag_approved": 1,
            "flag_deleted": 0,
            "flag_banned": 0,
            "flag_edit_users": 0,
            "flag_edit_system": 0,
            "flag_email_verified": 1,
            "share_email": 8,
            "email_bouncing": 0,
            "policy_class": 2,  # Public user. TODO: consider admin.
            "joined_date": joined_date,
            "joined_ip_num": ip_addr,
            "joined_remote_host": ip_addr
        },
        "nick": {
            "nickname": username,
            "flag_valid": 1,
            "flag_primary": 1
        },
        "profile": {
            "country": 'us',
            "affiliation": affiliation,
            "url": home_page,
            "type": random.randint(1, 5),
            "archive": archive,
            "subject_class": subject_class,
            "original_subject_classes": '',
            "flag_group_math": 1 if _prob(5) else 0,
            "flag_group_cs": 1 if _prob(5) else 0,
            "flag_group_nlin": 1 if _prob(5) else 0,
            "flag_group_q_bio": 1 if _prob(5) else 0,
            "flag_group_q_fin": 1 if _prob(5) else 0,
            "flag_group_stat": 1 if _prob(5) else 0
        },
        "password": {
            "password_storage": 2,
            "password_cleartext": password
        }
    }
    create_users({"users": [this]})


if __name__ == '__main__':
    cli()
