from flask import Flask
from jimmy import models, views, views_admin, views_auth


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('JIMMY_CONFIG')

    app.add_template_filter(views.semester_filter, 'semester')

    models.db.init_app(app)

    app.add_url_rule('/', 'home', views.home_page)
    app.add_url_rule('/semester/<int:year>/<int:half>/', 'semester', views.semester_view)

    # TODO: доделать формы редактирования и убрать админку
    # app.add_url_rule('/person/list/', 'person_list', views.person_list)
    # app.add_url_rule('/person/edit/<person_id>', 'person_edit', views.person_edit, methods=['GET', 'POST'])
    # app.add_url_rule('/job_assignment/list/', 'job_assignment_list', views.job_assignment_list)
    # app.add_url_rule('/student_group/list/', 'student_group_list', views.student_group_list)

    views_admin.init(app)

    views_auth.init(app)
    app.register_blueprint(views_auth.bp, url_prefix='/auth')

    return app
