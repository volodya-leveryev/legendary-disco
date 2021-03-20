from flask_admin.contrib.mongoengine import ModelView


class PersonView(ModelView):
    column_list = ('fio', 'emails', 'degree', 'title')
    column_default_sort = 'last_name'
    column_labels = {
        'fio': 'ФИО',
        'emails': 'Почта',
        'degree': 'Учёная степень',
        'title': 'Учёное звание',
    }


class TeacherView(ModelView):
    column_default_sort = 'person'
    column_labels = {
        'person': 'Преподаватель',
        'department': 'Кафедра',
        'position': 'Должность',
        'semester': 'Семестр',
        'wage_rate': 'Ставка',
    }


class StudentGroupView(ModelView):
    column_default_sort = 'name'
    column_labels = {
        'name': 'Название',
    }
