from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bankapp.auth import login_required
from bankapp.db import get_db

bp = Blueprint('account', __name__)

@bp.route('/')
def index():
    db = get_db()

    if g.user is not None:
        print('user id: ', g.user['id'])

    return render_template('account/index.html')

@bp.route('/transaction', methods=('GET', 'POST'))
@login_required
def transaction():
    return render_template('account/transaction.html')