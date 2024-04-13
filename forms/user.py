from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Введите имя пользователя в Telegram', validators=[DataRequired()])
    password = PasswordField('Введите ваш пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить вас?')
    submit = SubmitField('Выйти из залы...')


class RegisterForm(FlaskForm):
    login = StringField('Tg', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя Героя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
