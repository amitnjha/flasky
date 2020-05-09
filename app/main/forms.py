from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    password = PasswordField('What is your password?', validators=[DataRequired(),
                                                                   Length(min =  6, max=-1, message="Minumium 6")])
    submit = SubmitField('Submit')
