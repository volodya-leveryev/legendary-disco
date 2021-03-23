from flask import Flask
from flask_admin import Admin

from jimmy import models, views

admin = Admin()


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('JIMMY_CONFIG')

    models.db.init_app(app)

    views.oauth.init_app(app)
    azure_conf_url = 'https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0/.well-known/openid-configuration'
    azure_conf_url = azure_conf_url.format(**app.config)
    views.oauth.register('azure', server_metadata_url=azure_conf_url, client_kwargs={'scope': 'openid email'})
    google_conf_url = 'https://accounts.google.com/.well-known/openid-configuration'
    views.oauth.register('google', server_metadata_url=google_conf_url, client_kwargs={'scope': 'openid email'})

    app.add_url_rule('/login/', endpoint='login', view_func=views.login_page)
    app.add_url_rule('/azure_auth_init/', view_func=views.azure_auth_init)
    app.add_url_rule('/azure_auth_done/', view_func=views.azure_auth_done)
    app.add_url_rule('/google_auth_init/', view_func=views.google_auth_init)
    app.add_url_rule('/google_auth_done/', view_func=views.google_auth_done)
    app.add_url_rule('/logout/', view_func=views.logout)

    app.add_url_rule('/', endpoint='home', view_func=views.home_page)
    app.add_url_rule('/person/list/', endpoint='person_list', view_func=views.person_list)

    admin.init_app(app)
    admin.add_view(views.PersonView(models.Person, 'Люди'))
    admin.add_view(views.TeacherView(models.JobAssignment, 'Преподаватели'))
    admin.add_view(views.StudentGroupView(models.StudentGroup, 'Учебные группы'))

    return app
