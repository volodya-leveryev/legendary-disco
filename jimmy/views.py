""" Генерация HTML-страниц """
from flask import redirect, render_template, request, session, url_for

from jimmy.models import Course, semester_str


def semester_filter(semester_abs: int = 4042) -> str:
    """ Строковое представление семестра в шаблонах Jinja2 """
    return semester_str(semester_abs)


def login_required(func):
    """ Декоратор для принудительной аутентификации """
    def wrap(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login_page'))
        return func(*args, **kwargs)
    return wrap


@login_required
def semester_view(year, half):
    """ Возврат к странице после смены текущего семестра """
    session['sem'] = year * 2 + half - 1
    next_url = request.args.get('next', url_for('home'))
    return redirect(next_url)


@login_required
def home_page():
    """ Карточка учебных поручений преподавателя """
    courses = Course.objects.filter(teacher=session['user']['id'], semester_abs=session['sem'])
    return render_template('home.html', courses=courses)


@login_required
def course_list():
    """ Список курсов """
    courses = Course.objects.order_by('student_group', 'semester')
    return render_template('course_list.html', object_list=courses)


# TODO: доделать формы редактирования и убрать админку
# @login_required
# def person_list():
#     """ Список людей """
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
