from flask import Flask
from flask_admin import Admin
from flask_dance.contrib.google import make_google_blueprint

from jimmy import models, views


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('JIMMY_CONFIG')

    models.db.init_app(app)

    scope = ['openid', 'https://www.googleapis.com/auth/userinfo.email']
    auth_bp = make_google_blueprint(scope=scope)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    app.add_url_rule('/', endpoint='home', view_func=views.home_page)
    app.add_url_rule('/login/', endpoint='login', view_func=views.login_page)
    app.add_url_rule('/logout/', view_func=views.logout)

    admin = Admin(app)
    admin.add_view(views.PersonView(models.Person, 'Люди'))
    admin.add_view(views.TeacherView(models.JobAssignment, 'Преподаватели'))
    admin.add_view(views.StudentGroupView(models.StudentGroup, 'Учебные группы'))

    return app
