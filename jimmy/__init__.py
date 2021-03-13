from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from jimmy.models import db, migrate, User, Teacher, Assignment
from jimmy.views import TeacherView, AssignmentView


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    admin = Admin(app)
    admin.add_view(ModelView(User, db.session, 'Пользователь'))
    admin.add_view(TeacherView(Teacher, db.session, 'Преподаватель'))
    admin.add_view(AssignmentView(Assignment, db.session, 'Приём на работу'))

    return app
