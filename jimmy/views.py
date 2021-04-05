from xml.etree import ElementTree

from flask import redirect, render_template, request, session, url_for
from flask_admin import BaseView, expose
from flask_admin.contrib.mongoengine import ModelView


NAMESPACES = {
    'msdata': 'urn:schemas-microsoft-com:xml-msdata',
    'diffgr': 'urn:schemas-microsoft-com:xml-diffgram-v1',
    'mmisdb': 'http://tempuri.org/dsMMISDB.xsd',
}


def login_required(func):
    def wrap(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login_page'))
        return func(*args, **kwargs)
    return wrap


@login_required
def home_page():
    return render_template('home.html')


# TODO: доделать формы редактирования и убрать админку
# @login_required
# def person_list():
#     persons = models.Person.objects.order_by('last_name', 'first_name', 'second_name')
#     return render_template('person_list.html', persons=persons)


# TODO: доделать формы редактирования и убрать админку
# @login_required
# def person_edit(person_id):
#     person = models.Person.objects.get_or_404(id=person_id)
#     form = forms.PersonForm(obj=person)
#     return render_template('edit.html', form=form, title=person.fio)


# TODO: доделать формы редактирования и убрать админку
# @login_required
# def job_assignment_list():
#     job_assignments = models.JobAssignment.objects.order_by('person')
#     return render_template('job_assignment_list.html', job_assignments=job_assignments)


# TODO: доделать формы редактирования и убрать админку
# @login_required
# def student_group_list():
#     student_groups = models.StudentGroup.objects.order_by('name')
#     return render_template('student_group_list.html', student_groups=student_groups)


class Auth:
    def is_accessible(self):
        return 'user' in session

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login_page', next=request.url))


class LoadPlanView(Auth, BaseView):
    @expose('/')
    def index(self):
        return self.render('load_plan.html')


class PersonView(Auth, ModelView):
    column_list = ('fio', 'emails')
    column_default_sort = 'last_name,first_name,second_name'
    column_labels = {
        'fio': 'ФИО',
        'emails': 'Почта',
    }


class TeacherView(Auth, ModelView):
    column_default_sort = 'person'
    column_labels = {
        'person': 'Преподаватель',
        'department': 'Кафедра',
        'position': 'Должность',
        'wage_rate': 'Ставка',
    }


class StudentGroupView(Auth, ModelView):
    column_default_sort = 'name'
    column_labels = {
        'name': 'Название',
        'program': 'Программа',
        'subgroups': 'Подгруппы',
        'students': 'Студенты',
    }

    def load_plan(self, filename):
        root = ElementTree.parse(filename).getroot()
        plan = root.find('./{{{diffgr}}}diffgram/{{{mmisdb}}}dsMMISDB'.format(**NAMESPACES))


class CourseView(Auth, ModelView):
    column_default_sort = 'student_group,code'
    column_exclude_list = [
        'control',        # Форма контроля
        'hour_lecture',   # Лекции
        'hour_practice',  # Практические занятия
        'hour_lab_work',  # Лабораторные работы
        'hour_cons',      # Предэкзаменационные консультации
        'hour_exam',      # Экзамен
        'hour_test',      # Проверка РГР, рефератов и контрольных работ
        'hour_home',      # Проверка СРС
        'hour_rating',    # Ведение БРС
    ]
    column_labels = {
        'code': 'Код',
        'name': 'Название',
        'student_group': 'Учебная группа',
        'person': 'Преподаватель',
    }
