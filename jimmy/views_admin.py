from flask import Flask, session, redirect, request, url_for
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.menu import MenuLink
from werkzeug.datastructures import CombinedMultiDict

from jimmy.forms import RupForm
from jimmy.models import Course, EducationProgram, Person, StudentGroup, load_rup


def init(app: Flask) -> None:
    admin = Admin(name='Админка', template_mode='bootstrap3')
    admin.init_app(app)
    admin.add_view(LoadPlanView(name='Загрузка РУП', endpoint='load_plan'))
    admin.add_view(PersonView(Person, 'Люди'))
    admin.add_view(EducationProgramView(EducationProgram, 'Программы обучения'))
    admin.add_view(StudentGroupView(StudentGroup, 'Учебные группы'))
    admin.add_view(CourseView(Course, 'Курсы обучения'))
    admin.add_link(MenuLink(name='Сайт', url='/'))


class Auth:
    @staticmethod
    def is_accessible() -> bool:
        return 'user' in session

    @staticmethod
    def inaccessible_callback(_name, **_kwargs):
        return redirect(url_for('auth.login_page', next=request.url))


class LoadPlanView(Auth, BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = RupForm(CombinedMultiDict((request.files, request.form)))
        form.student_group.choices = [(sg.id, sg.name) for sg in StudentGroup.objects.all()]
        if form.validate_on_submit():
            sg_id = form.student_group.data
            student_group = StudentGroup.objects.get(id=sg_id)
            load_rup(form.rup_file.data, student_group)
            return redirect(url_for('admin.index'))
        return self.render('load_plan.html', form=form)


class EducationProgramView(Auth, ModelView):
    pass


class PersonView(Auth, ModelView):
    column_default_sort = [('last_name', False), ('first_name', False), ('second_name', False)]
    column_list = ('fio', 'emails', 'degree', 'title', 'job')


class StudentGroupView(Auth, ModelView):
    column_default_sort = [('program', False), ('year', False), ('name', False)]
    column_list = ('program', 'year', 'name', 'courses')


class CourseView(Auth, ModelView):
    column_default_sort = [('student_group', False), ('semester_abs', False)]
    column_filters = ('semester_abs',)
    column_list = ('student_group', 'code', 'name', 'semester_str', 'hour_lecture', 'hour_lab_work', 'hour_practice')
