from flask import redirect, render_template, request, session, url_for
from flask_admin import BaseView, expose
from flask_admin.contrib.mongoengine import ModelView, filters
from werkzeug.datastructures import CombinedMultiDict

from jimmy.forms import RupForm
from jimmy.models import StudentGroup, load_rup


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


class PersonView(Auth, ModelView):
    column_list = ('fio', 'emails')
    column_default_sort = [('last_name', False), ('first_name', False), ('second_name', False)]
    column_labels = {
        'fio': 'ФИО',
        'emails': 'Почта',
    }


class StudentGroupView(Auth, ModelView):
    column_default_sort = 'name'
    column_labels = {
        'name': 'Название',
        'program': 'Программа',
        'subgroups': 'Подгруппы',
        'students': 'Студенты',
    }


class CourseView(Auth, ModelView):
    column_default_sort = [('student_group', False), ('semester', False)]
    column_exclude_list = [
        'subject',
        'teacher',
    ]
    column_filters = ('semester',)
    column_labels = {
        'code': 'Код',
        'name': 'Название',
        'student_group': 'Учебная группа',
        'person': 'Преподаватель',
    }
