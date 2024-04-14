from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Введите имя пользователя в Telegram', validators=[DataRequired()])
    password = PasswordField('Введите ваш пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить вас?')
    submit = SubmitField('Выйти из зала...')


class RegisterForm(FlaskForm):
    login = StringField('Имя пользователя в Telegram', validators=[DataRequired()])
    password = PasswordField('Введите Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя Героя', validators=[DataRequired()])
    submit = SubmitField('Продолжить')
