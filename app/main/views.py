from datetime import datetime

from flask import render_template, session,redirect, url_for, request
from flask_login import login_required
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user =  User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data, password = form.password.data)
            db.session.add(user)
            db.session.commit()
            print('sending email')
            send_email('amitnjha@gmail.com', user.username,'frozen')
            print('sent!')
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',form = form,name = session.get('name'),known = session.get('known'),agent = request.headers.get('User-Agent'), current_time = datetime.utcnow())

@main.route('/secret')
@login_required
def secret():
    return 'Only Authenticated Users are allowed'


 
