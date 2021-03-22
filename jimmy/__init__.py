from flask import Flask
from flask_admin import Admin

from jimmy import models, views

admin = Admin()


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('JIMMY_CONFIG')

    models.db.init_app(app)

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    views.oauth.init_app(app)
    views.oauth.register('google', server_metadata_url=CONF_URL, client_kwargs={'scope': 'openid email'})

    app.add_url_rule('/', endpoint='home', view_func=views.home_page)
    app.add_url_rule('/login/', endpoint='login', view_func=views.login_page)
    app.add_url_rule('/auth/initiate/', view_func=views.auth_initiate)
    app.add_url_rule('/auth/complete/', view_func=views.auth_complete)
    app.add_url_rule('/auth/forget/', view_func=views.auth_forget)

    admin.init_app(app)
    admin.add_view(views.PersonView(models.Person, 'Люди'))
    admin.add_view(views.TeacherView(models.JobAssignment, 'Преподаватели'))
    admin.add_view(views.StudentGroupView(models.StudentGroup, 'Учебные группы'))

    return app
