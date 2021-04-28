from flask import redirect, render_template, request, session, url_for

from jimmy.models import Course


def semester_filter(s: int) -> str:
    if s and isinstance(s, int):
        year, half = divmod(s, 2)
    else:
        year, half = 2021, 0
    sem = 'осень' if half else 'весна'
    return f'{year}, {sem}'


def login_required(func):
    def wrap(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login_page'))
        return func(*args, **kwargs)
    return wrap


@login_required
def semester_view(year, half):
    session['sem'] = year * 2 + half - 1
    next_url = request.args.get('next', url_for('home'))
    return redirect(next_url)


@login_required
def home_page():
    courses = Course.objects.filter(teacher=session['user']['id'], semester=session['sem'])
    return render_template('home.html', courses=courses)


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
