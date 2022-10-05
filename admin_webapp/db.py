"""Db related functions."""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

def get_db(app:Flask) -> SQLAlchemy:
    """Gets the SQLAlchemy object for the flask app."""
    return app.extensions['sqlalchemy'].db
