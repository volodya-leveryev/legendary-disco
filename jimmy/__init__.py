from flask import Flask
from flask_admin import Admin

from jimmy.models import db, Person, Teacher
from jimmy.views import (PersonView, TeacherView)


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'
    app.config['MONGODB_HOST'] = 'localhost'
    app.config['MONGODB_DB'] = 'jimmy'
    db.init_app(app)

    admin = Admin(app)
    admin.add_view(PersonView(Person, 'Люди'))
    admin.add_view(TeacherView(Teacher, 'Преподаватели'))

    return app
