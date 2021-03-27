from flask import Flask
from flask_admin import Admin

from jimmy import auth, models, views

admin = Admin()


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('JIMMY_CONFIG')

    models.db.init_app(app)

    auth.init(app)
    app.register_blueprint(auth.bp, url_prefix='/auth')

    app.add_url_rule('/', 'home', views.home_page)
    app.add_url_rule('/person/list/', 'person_list', views.person_list)
    app.add_url_rule('/person/edit/<person_id>', 'person_edit', views.person_edit, methods=['GET', 'POST'])
    app.add_url_rule('/job_assignment/list/', 'job_assignment_list', views.job_assignment_list)
    app.add_url_rule('/student_group/list/', 'student_group_list', views.student_group_list)

    admin.init_app(app)
    admin.add_view(views.PersonView(models.Person, 'Люди'))
    admin.add_view(views.TeacherView(models.JobAssignment, 'Преподаватели'))
    admin.add_view(views.StudentGroupView(models.StudentGroup, 'Учебные группы'))

    return app
