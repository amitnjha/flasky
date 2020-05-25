from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField,SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp,ValidationError
from ..models import Role,User
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    password = PasswordField('What is your password?', validators=[DataRequired(),
                                                                   Length(min =  6, max=-1, message="Minumium 6")])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real Name', validators = [Length(0,64)])
    location =  StringField('Location', validators = [Length(0,64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Length(1,64), Email()])

    username = StringField('Username', validators=[
        DataRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or "underscror"')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce = int)
    name = StringField('Real Name', validators = [Length(0,64)])
    location =  StringField('Location', validators = [Length(0,64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self,field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use');
    

class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    body = StringField('',validators = [DataRequired()])
    submit = SubmitField('Submit')
