from flask import Flask, render_template, redirect, request, make_response, abort
from flask import session, jsonify
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
import datetime as dt
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Пароли разные')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Пользователь уже существует')
        if len(str(form.password.data)) < 6:
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Длина Пароля должна превышать 6')
        if len(set(str(form.password.data))) < 2:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Используйте в пароле не менее 3 разных символов')
        if form.password.data.isalpha():
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Используйте в пароле цифры')
        if form.password.data.isdigit():
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Используйте в пароле буквы')
        user = User(
            login=form.login.data,
            name=form.name.data,
            xp=0,
            level=1,
            inventory='',
            hands=1,
            body=2,
            legs=3,
            head=4
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', title='Авторизация',
                               message='Неверный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template("profile.html")


def main():
    db_session.global_init('db/blogs.db')
    app.run(port=8080)


if __name__ == '__main__':
    main()
