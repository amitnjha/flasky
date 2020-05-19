from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from . import auth
from .. import db
from ..email import send_email
from flask_login import current_user

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid user name or password')
    return render_template('auth/login.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your account', 'auth/email/confirm', user=user, token = token)
        
        flash('A confirmation email has been sent to you by email')
        return redirect(url_for('auth.login'))
    
    
    return render_template('auth/register.html', form = form)

@auth.route('confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('you have confirmed your account! Thanks!')
    else:
        flash('Confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))

@auth.route('unconfirmed')
def unconfirmed():
    return ('Your account is not confirmed. Please check you email for link')
    #return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        #if not current_user.confirmed and request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
        #    return redirect(url_for('auth.unconfirmed'))

