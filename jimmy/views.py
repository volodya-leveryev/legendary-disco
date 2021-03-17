from flask_admin.contrib.mongoengine import ModelView


class PersonView(ModelView):
    column_list = ('fio', 'emails', 'degree', 'title')
    column_labels = {
        'fio': 'ФИО',
        'emails': 'Почта',
        'degree': 'Учёная степень',
        'title': 'Учёное звание',
    }


class TeacherView(ModelView):
    column_labels = {
        'person': 'Преподаватель',
        'department': 'Кафедра',
        'position': 'Должность',
        'semester': 'Семестр',
        'wage_rate': 'Ставка',
    }
