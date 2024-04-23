from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, FileField, SubmitField, TextAreaField

from wtforms.validators import DataRequired


class ReportForm(FlaskForm):
    email = EmailField('Ваш Email', validators=[DataRequired()])
    name = StringField('Ваше Имя', validators=[DataRequired()])
    about = TextAreaField('Опишите Проблему', validators=[DataRequired()])
    file = FileField('Приложите Фото', validators=[DataRequired()])
    submit = SubmitField('Отправить обращение')
