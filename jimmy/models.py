from datetime import datetime
from io import TextIOBase
from typing import Dict, Union, List
from xml.etree import ElementTree

from flask_mongoengine import MongoEngine
from jellyfish import jaro_winkler_similarity
from mongoengine import (CASCADE, NULLIFY, BooleanField, DecimalField, DateTimeField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, IntField, ListField, ReferenceField, StringField)

db = MongoEngine()

NS_DIFFGR = 'urn:schemas-microsoft-com:xml-diffgram-v1'
NS_MMISDB = 'http://tempuri.org/dsMMISDB.xsd'

PLAN_SUBJECT = '2'
PLAN_PRACTICE = '3'

WT_LECTURE = 'Лек'
WT_LABWORK = 'Лаб'
WT_PRACTICE = 'Пр'
WT_CONTROLS = 'КСР'
WT_HOMEWORK = 'СР'
WT_EXAMS = 'Контроль'

CT_EXAM = 'Эк'
CT_CREDIT_GRADE = 'ЗаО'
CT_CREDIT = 'За'
CT_COURSEWORK = 'КП'

DEGREES = (
    ('к.арх.', 'Кандидат архитектуры'),
    ('к.б.н.', 'Кандидат биологических наук'),
    ('к.вет.н.', 'Кандидат ветеринарных наук'),
    ('к.воен.н.', 'Кандидат военных наук'),
    ('к.г.н.', 'Кандидат географических наук'),
    ('к.г.-м.н.', 'Кандидат геолого-минералогических наук'),
    ('к.иск.', 'Кандидат искусствоведения'),
    ('к.и.н.', 'Кандидат исторических наук'),
    ('к.культ.', 'Кандидат культурологии'),
    ('к.м.н.', 'Кандидат медицинских наук'),
    ('к.пед.н.', 'Кандидат педагогических наук'),
    ('к.полит.н.', 'Кандидат политических наук'),
    ('к.п.н.', 'Кандидат психологических наук'),
    ('к.с.-х.н.', 'Кандидат сельскохозяйственных наук'),
    ('к.социол.н.', 'Кандидат социологических наук'),
    ('к.теол.н.', 'Кандидат теологических наук'),
    ('к.т.н.', 'Кандидат технических наук'),
    ('к.фарм.н.', 'Кандидат фармацевтических наук'),
    ('к.ф.-м.н.', 'Кандидат физико-математических наук'),
    ('к.ф.н.', 'Кандидат филологических наук'),
    ('к.филос.н.', 'Кандидат философских наук'),
    ('к.х.н.', 'Кандидат химических наук'),
    ('к.э.н.', 'Кандидат экономических наук'),
    ('к.ю.н.', 'Кандидат юридических наук'),
    ('д.арх.', 'Доктор архитектуры'),
    ('д.б.н.', 'Доктор биологических наук'),
    ('д.вет.н.', 'Доктор ветеринарных наук'),
    ('д.воен.н.', 'Доктор военных наук'),
    ('д.г.н.', 'Доктор географических наук'),
    ('д.г.-м.н.', 'Доктор геолого-минералогических наук'),
    ('д.иск.', 'Доктор искусствоведения'),
    ('д.и.н.', 'Доктор исторических наук'),
    ('д.культ.', 'Доктор культурологии'),
    ('д.м.н.', 'Доктор медицинских наук'),
    ('д.пед.н.', 'Доктор педагогических наук'),
    ('д.полит.н.', 'Доктор политических наук'),
    ('д.п.н.', 'Доктор психологических наук'),
    ('д.с.-х.н.', 'Доктор сельскохозяйственных наук'),
    ('д.социол.н.', 'Доктор социологических наук'),
    ('д.теол.н.', 'Доктор теологических наук'),
    ('д.т.н.', 'Доктор технических наук'),
    ('д.фарм.н.', 'Доктор фармацевтических наук'),
    ('д.ф.-м.н.', 'Доктор физико-математических наук'),
    ('д.ф.н.', 'Доктор филологических наук'),
    ('д.филос.н.', 'Доктор философских наук'),
    ('д.х.н.', 'Доктор химических наук'),
    ('д.э.н.', 'Доктор экономических наук'),
    ('д.ю.н.', 'Доктор юридических наук'),
)

TITLES = (
    ('доц.', 'Доцент'),
    ('проф.', 'Профессор'),
)

POSITIONS = (
    ('асс.', 'Ассистент'),
    ('ст.пр.', 'Старший преподаватель'),
    ('доц.', 'Доцент'),
    ('доц.-исс.', 'Доцент-исследователь'),
    ('проф.', 'Профессор'),
    ('зав.каф.', 'Заведующий кафедрой'),
    ('зав.лаб.', 'Заведующий лабораторией'),
    ('зам.дир.', 'Заместитель директора'),
    ('нач.', 'Начальник'),
)

LEVEL = (
    ('Бак', 'Бакалавриат'),
    ('Маг', 'Магистратура'),
)

CONTROLS = (
    (CT_EXAM, 'Экзамен'),
    (CT_CREDIT_GRADE, 'Зачёт с оценкой'),
    (CT_CREDIT, 'Зачёт'),
    (CT_COURSEWORK, 'Курсовой проект'),
)


class Person(Document):
    """
    Человек и пользователь системы
    """

    class Degree(EmbeddedDocument):
        """
        Строка истории присуждения человеку учёных степеней
        """

        date = DateTimeField(verbose_name='Дата', required=True)
        degree = StringField(verbose_name='Уч. степень', required=True, choices=DEGREES)

    class Title(EmbeddedDocument):
        """
        Строка истории присвоения человеку учёных званий
        """

        date = DateTimeField(verbose_name='Дата', required=True)
        title = StringField(verbose_name='Уч. звание', required=True, choices=TITLES)

    class Job(EmbeddedDocument):
        """
        Строка истории трудоустройства человека
        """

        date = DateTimeField(verbose_name='Дата', required=True)
        department = ReferenceField('Department', verbose_name='Кафедра', on_delete=NULLIFY)
        position = StringField(verbose_name='Должность', required=True, choices=POSITIONS)
        wage_rate = DecimalField(verbose_name='Ставка', required=True)
        is_active = BooleanField(verbose_name='Работает', required=True)

        def __str__(self) -> str:
            return f'{self.wage_rate} {self.position} каф. {self.department}'

    last_name = StringField(verbose_name='Фамилия', required=True)
    first_name = StringField(verbose_name='Имя', required=True)
    second_name = StringField(verbose_name='Отчество')
    maiden_name = StringField(verbose_name='Девичья фамилия')
    emails = ListField(StringField(), verbose_name='Почта')
    is_user = BooleanField(verbose_name='Пользователь')
    is_admin = BooleanField(verbose_name='Администратор')
    student_num = StringField(verbose_name='Номер студ. билета')
    degree_history = ListField(EmbeddedDocumentField(Degree), verbose_name='Уч. степень')
    title_history = ListField(EmbeddedDocumentField(Title), verbose_name='Уч. звание')
    job_history = ListField(EmbeddedDocumentField(Job), verbose_name='Должность')
    person_id = IntField(verbose_name='Ключ человека в старой БД')
    user_id = IntField(verbose_name='Ключ пользователя в старой БД')
    # Нужно добавить courses_history для ведения истории повышения квалификации

    @property
    def degree(self) -> str:
        degree_list = sorted(self.degree_history, key=lambda t: t.date)[-1:]
        return degree_list[0].degree if degree_list else ''

    @property
    def title(self) -> str:
        title_list = sorted(self.title_history, key=lambda t: t.date)[-1:]
        return title_list[0].title if title_list else ''

    @property
    def job(self) -> str:
        active_jobs = filter(lambda j: j.is_active, self.job_history)
        sorted_jobs = sorted(active_jobs, key=lambda j: j.wage_rate, reverse=True)
        return ', '.join(map(str, sorted_jobs))

    @property
    def fio(self) -> str:
        result = f'{self.last_name} {self.first_name:.1}.'
        if self.second_name:
            result += f' {self.second_name:.1}.'
        return result

    def __str__(self):
        return self.fio


class Department(db.Document):
    """
    Кафедра
    """

    name = StringField(verbose_name='Название', required=True)
    short = StringField(verbose_name='Сокращение')
    organization = StringField(verbose_name='Институт')
    code = IntField(verbose_name='Код')
    depart_id = IntField(verbose_name='Ключ кафедры в старой БД')

    def __str__(self):
        if self.short:
            return f'{self.short} {self.organization}'
        else:
            return f'{self.name}'


class EducationProgram(db.Document):
    """
    Образовательная программа
    """

    code = StringField(verbose_name='Код', required=True)
    name = StringField(verbose_name='Название', required=True)
    short = StringField(verbose_name='Сокращение', required=True)
    level = StringField(verbose_name='Уровень', required=True, choices=LEVEL)

    def __str__(self):
        return f'{self.level} {self.short}'


class StudentGroup(Document):
    """
    Учебная группа студентов
    """

    class Subgroups(EmbeddedDocument):
        """
        Строка истории изменения количества подгрупп
        """

        date = DateTimeField(verbose_name='Дата')
        count = IntField(verbose_name='Количество', requred=True)

    class Students(EmbeddedDocument):
        """
        Строка истории изменения количества студентов
        """

        date = DateTimeField(verbose_name='Дата')
        count = IntField(verbose_name='Количество', requred=True)

    name = StringField(verbose_name='Название', required=True)
    year = IntField(verbose_name='Год поступления', required=True)
    program = ReferenceField('EducationProgram', verbose_name='Программа', required=True, on_delete=NULLIFY)
    subgroups_history = ListField(EmbeddedDocumentField(Subgroups), verbose_name='Подгруппы')
    students_history = ListField(EmbeddedDocumentField(Students), verbose_name='Студенты')

    def subgroups(self, semester_abs: int) -> int:
        """ Количество подгрупп в семестре """
        year, half = divmod(semester_abs, 2)
        border = datetime(year + half, 1 if half else 6, 1)
        subgroups_list = filter(lambda s: s.date < border, self.subgroups_history)
        subgroups_list = sorted(subgroups_list, key=lambda t: t.date)[-1:]
        return subgroups_list[0].count if subgroups_list else 0

    @property
    def students(self) -> int:
        students_list = sorted(self.students_history, key=lambda t: t.date)[-1:]
        return students_list[0].count if students_list else 0

    @property
    def courses(self) -> int:
        return len(Course.objects(student_group=self))

    def get_education_year(self, semester_abs: int) -> int:
        """ Курс (год) обучения """
        return (semester_abs - int(self.year) * 2 - 1) // 2 + 1

    def __str__(self):
        return f'{self.name}'


class Subject(Document):
    """
    Дисциплина
    Может вестись у нескольких групп и идти несколько семестров
    Пока не используется
    """

    name = StringField(verbose_name='Название', required=True)


class Course(Document):
    """
    Курс для учебной группы в одном семестре
    Если предмет идёт у разных групп — создаем несколько записей
    Если предмет идёт несколько семестров — создаем несколько записей
    Если имеет несколько форм контроля — создаем несколько элементов в списке controls
    """

    student_group = ReferenceField('StudentGroup', verbose_name='Учеб. группа', required=True, on_delete=CASCADE)
    semester_abs = IntField(verbose_name='Семестр', required=True)
    code = StringField(verbose_name='Код', required=True)
    name = StringField(verbose_name='Название', required=True)

    # Эти поля загружаются из РУП
    hour_lecture = IntField(verbose_name='Лекции')        # Лекции
    hour_practice = IntField(verbose_name='Практики')     # Практические занятия
    hour_lab_work = IntField(verbose_name='Лаб. работы')  # Лабораторные работы
    hour_exam = IntField(verbose_name='Часы экз.')        # Экзамен
    hour_homework = IntField(verbose_name='СРС')          # СРС
    control = IntField(verbose_name='КСР')                # Контроль СР
    controls = ListField(StringField(choices=CONTROLS), verbose_name='Форма контроля')

    # Эти значения проставляет заведующий кафедрой
    # hour_cons = IntField(verbose_name='Предэкз. конс.')   # Предэкзаменационные консультации
    # hour_test = IntField(verbose_name='Проверка КР')      # Проверка РГР, рефератов и КР
    # hour_rating = IntField(verbose_name='БРС')            # Ведение БРС
    subject = ReferenceField('Subject', verbose_name='Дисциплина', on_delete=NULLIFY)
    teacher = ReferenceField('Person', verbose_name='Преподаватель', on_delete=NULLIFY)

    @property
    def sem(self) -> int:
        return self.semester_abs - 2 * self.student_group.year

    @property
    def year(self) -> int:
        return self.sem // 2

    @property
    def semester_str(self) -> str:
        return semester_str(self.semester_abs)

    def hour_cons(self, ) -> int:
        res = 100500
        if CT_EXAM in self.controls:
            res = min(self.hour_exam)
        return res

    def __str__(self):
        return f'{self.student_group}, {self.sem}: {self.name}'


def semester_str(semester_abs: int) -> str:
    """ Строковое представление семестра """
    year, half = divmod(semester_abs, 2)
    sem = 'осень' if half else 'весна'
    return f'{year}, {sem}'


def get_subjects(rup: TextIOBase) -> List[Dict[str, Union[str, Dict[int, Dict[str, int]]]]]:
    """ Читаем данные РУП из файла PLX """

    root = ElementTree.fromstring(rup.read())
    plan = root.find(f'./{{{NS_DIFFGR}}}diffgram/{{{NS_MMISDB}}}dsMMISDB')

    # Читаем справочник видов работ, он пригодится
    work_abbr = {}
    for work_type_elem in plan.findall(f'./{{{NS_MMISDB}}}СправочникВидыРабот'):
        work_code = work_type_elem.attrib['Код']
        work_abbr[work_code] = work_type_elem.attrib['Аббревиатура']

    # Читаем дисциплины и практики
    subjects = {}
    for subj_elem in plan.findall(f'./{{{NS_MMISDB}}}ПланыСтроки'):
        if subj_elem.attrib['ТипОбъекта'] not in (PLAN_SUBJECT, PLAN_PRACTICE):
            continue
        subjects[subj_elem.attrib['Код']] = {
            'code': subj_elem.attrib['ДисциплинаКод'],
            'name': subj_elem.attrib['Дисциплина'],
            'semesters': {},
        }

    # Читаем трудоемкость дисциплин по семестрам и видам работ
    path = f'./{{{NS_MMISDB}}}ПланыНовыеЧасы[@КодТипаЧасов="1"]'
    for hour_elem in plan.findall(path):
        subject = subjects.get(hour_elem.attrib['КодОбъекта'])
        if subject is None:
            continue
        year = int(hour_elem.attrib['Курс'])
        semester = (year - 1) * 2 + int(hour_elem.attrib['Семестр'])
        work_type = work_abbr[hour_elem.attrib['КодВидаРаботы']]
        subject['semesters'].setdefault(semester, {})
        subject['semesters'][semester][work_type] = int(hour_elem.attrib['Количество'])

    return list(subjects.values())


def load_rup(rup: TextIOBase, student_group: StudentGroup) -> None:
    """ Загрузка данных курсов из файлов РУП """

    # Читаем данные РУП из файла PLX
    subjects = get_subjects(rup)

    # Запоминаем существующие курсы
    old_courses = list(Course.objects(student_group=student_group))

    # Просматриваем дисциплины и их трудоемкость по семестрам
    for subject in subjects:
        for semester, hours in subject['semesters'].items():

            # Просматриваем существующие курсы данной группы
            courses_pool = [(Course(), -1)]
            for oc in old_courses:
                # Чтобы ускорить работу берём только похожие
                old_course_signature = oc.name + str(oc.semester_abs - oc.student_group.year * 2)
                new_course_signature = str(subject['name']) + str(semester)
                distance = jaro_winkler_similarity(old_course_signature, new_course_signature)
                threshold = 0.9
                if distance > threshold:
                    courses_pool.append((oc, distance))

            # Сортируем по редакционному расстоянию, если нет похожих - берём новый курс
            courses_pool.sort(key=lambda pair: pair[1], reverse=True)
            course = courses_pool[0][0]
            if courses_pool[0][1] != -1:
                old_courses.remove(course)

            # Заполняем данные курса
            course.student_group = student_group
            course.semester_abs = student_group.year * 2 + semester
            course.code = subject['code']
            course.name = subject['name']
            course.hour_lecture = hours.get(WT_LECTURE, 0)
            course.hour_practice = hours.get(WT_PRACTICE, 0)
            course.hour_lab_work = hours.get(WT_LABWORK, 0)
            course.hour_exam = hours.get(WT_EXAMS, 0)
            course.hour_homework = hours.get(WT_HOMEWORK, 0)
            course.control = hours.get(WT_CONTROLS, 0)
            course.controls = []
            for control in (CT_EXAM, CT_CREDIT, CT_COURSEWORK, CT_CREDIT_GRADE):
                if control in hours:
                    course.controls.append(control)
            course.save()

    # Удаляем неиспользованные курсы
    for oc in old_courses:
        oc.delete()
