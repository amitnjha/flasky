from datetime import datetime

from flask import render_template, session,redirect, url_for, request, flash
from flask_login import login_required
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..models import User, Permission, Role,Post
from ..email import send_email
import os
import json
import random
from flask import Response
from ..decorators import admin_required, permission_required
from flask_login import current_user
from ..decorators import admin_required

size_list = [0.5, 1, 2]

@main.route('/', methods=['GET', 'POST'])
def index():
    #form = NameForm()
    #if form.validate_on_submit():
    #    user =  User.query.filter_by(username = form.name.data).first()
    #    if user is None:
    #        user = User(username = form.name.data, password = form.password.data)
    #        db.session.add(user)
    #        db.session.commit()
    #        print('sending email')
    #        send_email('amitnjha@gmail.com', user.username,'frozen')
    #        print('sent!')
    #        session['known'] = False
    #    else:
    #        session['known'] = True
    #    session['name'] = form.name.data
    #    form.name.data = ''
    #    return redirect(url_for('.index'))
    #return render_template('index.html',form = form,name = session.get('name'),known = session.get('known'),agent = request.headers.get('User-Agent'), current_time = datetime.utcnow())
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post()
        post.body = form.body.data
        post.author_id=current_user._get_current_object().id
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form = form, posts = posts)


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

@main.route('/edit-profile/<int:id>', methods = ['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated')
        return redirect(url_for('.user',username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form = form, user = user)
