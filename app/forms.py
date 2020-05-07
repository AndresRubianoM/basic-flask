from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('User Name', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Enviar')


class TodoForm(FlaskForm):
    description = StringField('Desciption', validators = [DataRequired()])
    submit = SubmitField('Create')

class DeleteTodoForm(FlaskForm):
    submit = SubmitField('delete')

class UpdateTodoForm(FlaskForm):
    submit = SubmitField('Update')
