import json

from flask import redirect, render_template, request, session, url_for
from flask_admin.contrib.mongoengine import ModelView
from flask_dance.contrib.google import google

from jimmy.models import Person


def login_required(func):
    def wrap(*args, **kwargs):
        if not google.authorized:
            return redirect(url_for('login'))
        if 'user' not in session:
            userinfo = json.loads(google.get('/oauth2/v1/userinfo').content)
            persons = Person.objects(emails=userinfo.get('email'))
            if not persons:
                return redirect(url_for('login'))
            session['user'] = {
                'id': str(persons[0].id),
                'str': str(persons[0]),
            }
        return func(*args, **kwargs)
    return wrap


@login_required
def home_page():
    return render_template('index.html')


def login_page():
    return render_template('login.html')


def logout():
    session.pop('google_oauth_token')
    session.pop('user')
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
