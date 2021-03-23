from authlib.integrations.flask_client import OAuth
from flask import redirect, render_template, request, session, url_for
from flask_admin.contrib.mongoengine import ModelView

from jimmy import models

oauth = OAuth()


def login_required(func):
    def wrap(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrap


@login_required
def home_page():
    return render_template('index.html')


def login_page():
    return render_template('login.html')


def azure_auth_init():
    scheme = request.headers.get('X-Forwarded-Proto')
    redirect_uri = url_for('azure_auth_done', _external=True, _scheme=scheme)
    return oauth.azure.authorize_redirect(redirect_uri)


def azure_auth_done():
    token = oauth.azure.authorize_access_token()
    userinfo = oauth.azure.parse_id_token(token)
    persons = models.Person.objects(emails=userinfo.get('email'))
    if not persons:
        return redirect(url_for('login'))
    session['user'] = {
        'id': str(persons[0].id),
        'str': str(persons[0]),
    }
    return redirect(url_for('home'))


def google_auth_init():
    scheme = request.headers.get('X-Forwarded-Proto')
    redirect_uri = url_for('google_auth_done', _external=True, _scheme=scheme)
    return oauth.google.authorize_redirect(redirect_uri)


def google_auth_done():
    token = oauth.google.authorize_access_token()
    userinfo = oauth.google.parse_id_token(token)
    persons = models.Person.objects(emails=userinfo.get('email'))
    if not persons:
        return redirect(url_for('login'))
    session['user'] = {
        'id': str(persons[0].id),
        'str': str(persons[0]),
    }
    return redirect(url_for('home'))


def logout():
    session.clear()
    return redirect(url_for('login'))


class PersonView(ModelView):
    column_list = ('fio', 'emails', 'degree', 'title')
    column_default_sort = 'last_name'
    column_labels = {
        'fio': 'ФИО',
        'emails': 'Почта',
        'degree': 'Учёная степень',
        'title': 'Учёное звание',
    }

    def is_accessible(self):
        return 'user' in session

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class TeacherView(ModelView):
    column_default_sort = 'person'
    column_labels = {
        'person': 'Преподаватель',
        'department': 'Кафедра',
        'position': 'Должность',
        'semester': 'Семестр',
        'wage_rate': 'Ставка',
    }

    def is_accessible(self):
        return 'user' in session

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class StudentGroupView(ModelView):
    column_default_sort = 'name'
    column_labels = {
        'name': 'Название',
    }

    def is_accessible(self):
        return 'user' in session

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
