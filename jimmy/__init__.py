import os

from flask import Flask
from flask_admin import Admin

from jimmy.models import db, Person, JobAssignment, StudentGroup
from jimmy.views import (PersonView, TeacherView, StudentGroupView)


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('APP_SECRET', 'secret')
    app.config['MONGODB_HOST'] = os.environ.get('APP_DB_HOST', 'localhost')
    app.config['MONGODB_DB'] = 'jimmy'
    db.init_app(app)

    admin = Admin(app)
    admin.add_view(PersonView(Person, 'Люди'))
    admin.add_view(TeacherView(JobAssignment, 'Преподаватели'))
    admin.add_view(StudentGroupView(StudentGroup, 'Учебные группы'))

    return app
