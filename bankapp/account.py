from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file
)
from werkzeug.exceptions import abort

from bankapp.auth import login_required
from bankapp.db import get_db

import re, os

bp = Blueprint('account', __name__)

@bp.route('/')
def index():
    # If user doesn't login, go to login page
    if g.user is None:
        return redirect(url_for('auth.login', target=''))

    # otherwise, go to home page
    return render_template('account/index.html')

@bp.route('/download_user_image')
@login_required
def download_user_image():
    image_id = request.args.get('image_id')
    images_path = os.path.dirname(os.path.abspath(__file__))

    if image_id == None:
        # user_image_path = os.path.join(images_path, 'images', str(g.user['id']) + '.jpg')
        user_image_path = os.path.join(images_path, 'images', 'default.jpg')
    else:
        user_image_path = images_path + '/' + 'images' + '/' + image_id

    return send_file(user_image_path, as_attachment=True)

@bp.route('/show_balance', methods=('GET', 'POST'))
@login_required
def show_balance():
    if request.method == 'GET':
        db = get_db()
        balance = db.execute(
            'SELECT balance FROM account WHERE user_id = ?', (g.user['id'],)
        ).fetchone()
        
    return render_template('account/show_balance.html', balance = "{:.2f}".format(balance['balance']))

@bp.route('/transaction', methods=('GET', 'POST'))
@login_required
def transaction():
    if request.method == 'GET':
        db = get_db()
        balance = db.execute(
            'SELECT balance FROM account WHERE user_id = ?', (g.user['id'],)
        ).fetchone()
        
        return render_template('account/transaction.html', balance = "{:.2f}".format(balance['balance']))

    if request.method == 'POST':
        deposit_amount = request.form['deposit_amount']
        withdraw_amount = request.form['withdraw_amount']
        action = request.form['deposit-withdraw']

        db = get_db()
        result_msg = None
        regex_amount = re.compile('0\\.[0-9]{2}|[1-9][0-9]*\\.[0-9]{2}')

        balance = db.execute(
            'SELECT balance FROM account WHERE user_id = ?', (g.user['id'],)
        ).fetchone()

        if action == "deposit":
            if regex_amount.fullmatch(deposit_amount) is None or float(deposit_amount)  > 4294967295.99:
                result_msg = 'Not a valid deposit or withdrawal amount.'
                return render_template('account/transaction-result.html', result_msg = result_msg, balance = "{:.2f}".format(balance['balance']))
            else:      
                updated_balance = balance['balance'] + float(deposit_amount)       
                db.execute('UPDATE account SET balance = ? WHERE user_id = ?', (updated_balance, g.user['id'],))
                db.commit()
        else:
            if regex_amount.fullmatch(withdraw_amount) is None or float(withdraw_amount)  > 4294967295.99:
                result_msg = 'Not a valid deposit or withdrawal amount.'
                return render_template('account/transaction-result.html', result_msg = result_msg, balance = "{:.2f}".format(balance['balance']))
            else:
                updated_balance = balance['balance'] - float(withdraw_amount)
                if updated_balance < 0:
                    result_msg = 'Insufficient Balance.'
                    return render_template('account/transaction-result.html', result_msg = result_msg, balance = "{:.2f}".format(balance['balance']))
                else:
                    db.execute('UPDATE account SET balance = ? WHERE user_id = ?', (updated_balance, g.user['id'],))
                    db.commit()

        return render_template('account/transaction-result.html', result_msg = "Success", balance = "{:.2f}".format(updated_balance))


@bp.route('/transaction-result', methods=('GET', 'POST'))
@login_required
def transaction_result():
    return render_template('account/transaction-result.html')