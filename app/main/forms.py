from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length

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

