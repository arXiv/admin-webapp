"""Jinja2 templating filters"""
from datetime import datetime

def unix_to_datetime(unix_time):
    return datetime.utcfromtimestamp(unix_time)
