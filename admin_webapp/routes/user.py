"""arXiv user routes."""

from flask import Blueprint, render_template, url_for, request, \
    make_response, redirect, current_app, send_file, Response, flash

from flask_sqlalchemy import get_state, Pagination

from sqlalchemy import select, func
from arxiv.base import logging

from arxiv_auth.auth.decorators import scoped


blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/<int:id>', methods=['GET'])
def display() -> Response:
    return render_template('user/display.html')
