from flask_sqlalchemy import SQLAlchemy
from flask import Flask

def get_db(app:Flask) -> SQLAlchemy:
    return app.extensions['sqlalchemy']
