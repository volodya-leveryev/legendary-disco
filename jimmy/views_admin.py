""" Генерация HTML-страниц для админки """
from flask import Flask, session, redirect, request, url_for
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.menu import MenuLink
from werkzeug.datastructures import CombinedMultiDict

from jimmy import forms, models


def init(app: Flask) -> None:
    """ Инициализация админки """
    admin = Admin(name='Админка', template_mode='bootstrap3')
    admin.init_app(app)
    admin.add_view(LoadPlanView(name='Загрузка РУП', endpoint='load_plan'))
    admin.add_view(PersonView(models.Person, 'Люди'))
    admin.add_view(StudentGroupView(models.StudentGroup, 'Учебные группы'))
    admin.add_view(CourseView(models.Course, 'Курсы обучения'))
    admin.add_view(DepartmentView(models.Department, 'Кафедры'))
    admin.add_view(AdmissionHistoryView(models.AdmissionHistory, 'Зачисления студентов'))
    admin.add_link(MenuLink(name='Сайт', url='/'))


class Auth:
    """ Абстрактный базовый класс-миксин для принудительной авторизации """
    @staticmethod
    def is_accessible() -> bool:
        """ Авторизирован ли пользователь """
        return 'user' in session

    @staticmethod
    def inaccessible_callback(_name, **_kwargs):
        """ Перенаправление на страницу авторизации """
        return redirect(url_for('auth.login_page', next=request.url))


class LoadPlanView(Auth, BaseView):
    """ Загрузка учебного плана """
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        """ Страница для получения файла с учебным планом """
        form = forms.RupForm(CombinedMultiDict((request.files, request.form)))
        student_groups = models.StudentGroup.objects
        form.student_group.choices = [(sg.id, sg.name) for sg in student_groups.all()]
        if form.validate_on_submit():
            sg_id = form.student_group.data
            student_group = student_groups.get(id=sg_id)
            models.load_rup(form.rup_file.data, student_group)
            return redirect(url_for('admin.index'))
        return self.render('load_plan.html', form=form)


class DepartmentView(Auth, ModelView):
    """ Кафедры """
    # column_default_sort = [('organization', False), ('code', False), ('name', False)]
    column_default_sort = [('depart_id', False)]


class PersonView(Auth, ModelView):
    """ Люди """
    column_default_sort = [('last_name', False), ('first_name', False), ('second_name', False)]
    column_list = ('fio', 'emails', 'job', 'student_group')


class AdmissionHistoryView(Auth, ModelView):
    """ История зачисления студентов в группы """
    column_default_sort = [('group', False), ('student', False)]
    column_list = ('group', 'student', 'beg', 'end')


class StudentGroupView(Auth, ModelView):
    """ Учебные группы """
    column_default_sort = [('year', False), ('program_code', False), ('name', False)]
    column_list = ('year', 'program_code', 'name', 'courses', 'group_id')


class CourseView(Auth, ModelView):
    """ Курсы обучения """
    column_default_sort = [('student_group', False), ('semester_abs', False)]
    column_filters = ('semester_abs',)
    column_list = ('student_group', 'code', 'name', 'semester_str', 'hour_lecture', 'hour_lab_work', 'hour_practice')
