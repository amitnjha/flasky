from datetime import datetime

from flask import render_template, session,redirect, url_for, request, flash
from flask_login import login_required
from . import main
from .forms import NameForm, EditProfileForm
from .. import db
from ..models import User, Permission
from ..email import send_email
import os
import json
import random
from flask import Response
from ..decorators import admin_required, permission_required
from flask_login import current_user

size_list = [0.5, 1, 2]

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

@main.route('/images', methods=['GET', 'POST'])
def images():
    imgList = []
    imgs = os.listdir('/var/www/html/images')
    for img in imgs:
        size = random.randint(1,4)
        imgList.append({"src":"https://aditijha.org/images/"+img, "width": size, "height":size, "dummy": "dummy"})
    #print(imgList)
    return Response(json.dumps(imgList), mimetype='text/json')

@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return 'For Administrators'


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderator_only():
    return 'For comment moderators'


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template('user.html', user = user)

@main.route('/edit-profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data =current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form = form)
