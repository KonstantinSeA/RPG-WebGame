from flask import Flask, render_template, redirect, request, make_response, abort
from flask import session, jsonify
from data import db_session
from data.users import User
from data.items import Item
from forms.user import RegisterForm, LoginForm
from forms.report import ReportForm
import datetime as dt
import schedule
import time
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from flask_restful import reqparse, abort, Api, Resource
from other_py_files.some_function import equip, shedule_settings
from other_py_files.game import game_request, get_answer, after_await


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
    db_sess = db_session.create_session()
    db_users = db_sess.query(User).all()
    users = []
    for user in db_users:
        users.append([user.name, user.level, user.xp])
    return \
        render_template("index.html", users=sorted(users, key=lambda x: (x[1], x[2]), reverse=True))


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
            head=4,
            energy=10,
            icon_name='standart.jpg'
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


@app.route('/equip/<position>/<int:item_id>')
def equip_item(position, item_id):
    equip(position, item_id, current_user.id)
    return redirect('/inventory')


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


@app.route('/support', methods=['GET', 'POST'])
def support():
    form = ReportForm()
    if form.validate_on_submit():
        f = form.file.data
        if not (f.filename.endswith('.jpg') or f.filename.endswith('.png')):
            return render_template("support_form.html",
                                   message='Приложите Фото, а не другой файл', form=form)
        f.save(f'reports/{f.filename}')
        report = [f'Email: {form.email.data}\n', f'Name: {form.name.data}\n\n',
                  form.about.data, f'\n\nPhoto: {f.filename}\n']
        with open(f'reports/{form.name.data}', mode='w') as fod:
            fod.writelines(report)
        return render_template("support_form.html", message='Обращение Отправлено', form=form)

    return render_template("support_form.html", form=form)


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    db_sess = db_session.create_session()
    all_items = db_sess.query(Item).all()
    items = []
    for x in current_user.inventory.split(', '):
        try:
            items.append((all_items[int(x) - 1].name, all_items[int(x) - 1].position,
                          all_items[int(x) - 1].about, all_items[int(x) - 1].id))
        except ValueError:
            break
    equipment = [(all_items[current_user.head - 1].name,
                  all_items[current_user.head - 1].about, all_items[current_user.head - 1].id),
                 (all_items[current_user.body - 1].name,
                  all_items[current_user.body - 1].about, all_items[current_user.body - 1].id),
                 (all_items[current_user.legs - 1].name,
                  all_items[current_user.legs - 1].about, all_items[current_user.legs - 1].id),
                 (all_items[current_user.hands - 1].name,
                  all_items[current_user.hands - 1].about, all_items[current_user.hands - 1].id)]
    return render_template("inventory.html", rows_n=len(items) // 4,
                           no_rows=len(items) % 4, items=items, equipment=equipment)


def main():
    db_session.global_init('db/blogs.db')
    app.run(port=5000)
    shedule_settings()
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
