import functools
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bankapp.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register-start', methods=('GET', 'POST'))
def register_start():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None

        regex_chars = re.compile('[_\\-\\.0-9a-z]+')

        if not username:
            error = 'User name is required.'
        elif len(username) > 127:
            error = 'User name is too long.'
        elif regex_chars.fullmatch(username) == None:
            error = 'User name contains illegal characters.'

        if error is None:
            session['username'] = username
            return redirect(url_for('auth.register', username_register=username))

        flash(error)
    return render_template('auth/register-start.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    username = request.args.get('username_register')

    if request.method == 'POST':
        password = request.form['password']
        phone_number = request.form['phone_number']
        initial_amount = request.form['initial_amount']
        db = get_db()
        error = None

        regex_chars = re.compile('[_\\-\\.0-9a-z]+')
        regex_amount = re.compile('0\\.[0-9]{2}|[1-9][0-9]*\\.[0-9]{2}')

        # Check if the front-end does not prevent empty fields
        if not username:
            error = 'User name is required.'
        elif not password:
            error += 'Password is required.'
        elif phone_number.isnumeric() == False or len(phone_number) != 10:
            error = 'Phone number is required and should be numeric and 10 digital numbers'
        elif regex_amount.fullmatch(initial_amount) is None or float(initial_amount)  > 4294967295.99:
            error = 'Not a valid deposit or withdrawal amount'

        if (len(username) > 127):
            error = 'User name is too long.'
        elif (regex_chars.fullmatch(username) == None):
            error = 'User name contains illegal characters.'

        if (len(password) > 127):
            error = 'Password is too long.'
        elif (regex_chars.fullmatch(password) == None):
            error = 'Password contains illegal characters.'

        find_user_ps = 'SELECT id FROM user WHERE username = ?'
        if db.execute(find_user_ps, (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password, phone_number) VALUES (?, ?, ?)',
                    (username, generate_password_hash(password), phone_number),
                )
                db.commit()

                user_id_query = db.execute(find_user_ps, (username,)).fetchone()
                user_id = user_id_query['id']
                db.execute(
                    'INSERT INTO account (user_id, balance) VALUES (?, ?)',
                    (user_id, initial_amount)
                )
                db.commit()

            except db.IntegrityError:
                error = f'Unknown server error'
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    session['username'] = username
    return render_template('auth/register.html', username=username)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username or password'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username or password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)

    if request.method == 'GET':
        # Check if the user login or not. If login, redirect to home
        if g.user is not None:
            return redirect(url_for('index'))

    target = request.args.get('target')
    # if target param exist, use a whitelist redirect function to decide redirection
    if target and len(target) > 0:
        return check_redirect(target)
    return render_template('auth/login.html')

def check_redirect(target):
    whilte_list = ['https://uci.edu']

    # Check if target is whitelist
    if target.startswith('http:') or target.startswith('https://'):
        if target in whilte_list:
            print('This is in white_list, do redirection')
            return redirect(target)
        else:
            print('This is not in white_list, do nothing')
            return

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view