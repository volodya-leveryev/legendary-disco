from typing import Dict, Union, List
from xml.etree import ElementTree

from flask_mongoengine import MongoEngine
from jellyfish import jaro_winkler_similarity
from mongoengine import CASCADE, NULLIFY

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


class Degree(db.EmbeddedDocument):
    """
    Учёные степени
    Вспомогательный документ для ведения истории присуждения человеку учёных степеней
    """
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
    date = db.DateTimeField(verbose_name='Дата')
    degree = db.StringField(verbose_name='Уч. степень', max_length=16, choices=DEGREES)


class Title(db.EmbeddedDocument):
    """
    Учёные звания
    Вспомогательный документ для ведения истории присвоения человеку учёных званий
    """
    TITLES = (
        ('доц.', 'Доцент'),
        ('проф.', 'Профессор'),
    )
    date = db.DateTimeField(verbose_name='Дата')
    title = db.StringField(verbose_name='Уч. звание', max_length=8, choices=TITLES)


class Job(db.EmbeddedDocument):
    """
    Должности
    Вспомогательный документ для ведения истории трудоустройства человека
    """
    DEPARTMENTS = (
        ('АиГ', 'Кафедра алгебры и геометрии'),
        ('ВМ', 'Кафедра высшей математики'),
        ('ДУ', 'Кафедра дифференциальных уравнений'),
        ('ИТ', 'Кафедра информационных технологий'),
        ('МЭПИ', 'Кафедра математической экономики и прикладной информатики'),
        ('МА', 'Кафедра математического анализа'),
        ('МПМ', 'Кафедра методики преподавания математики'),
        ('МТС', 'Кафедра многоканальных телекоммуникационных систем'),
        ('ПМ', 'Кафедра прикладной математики'),
        ('ТМОИ', 'Кафедра теории и методики обучения информатики'),
    )

    POSITIONS = (
        ('асс.', 'Ассистент'),
        ('ст.пр.', 'Старший преподаватель'),
        ('доц.', 'Доцент'),
        ('проф.', 'Профессор'),
        ('зав.каф.', 'Заведующий кафедрой'),
    )

    date = db.DateTimeField(verbose_name='Дата')
    department = db.StringField(verbose_name='Кафедра', max_length=5, required=True, choices=DEPARTMENTS)
    position = db.StringField(verbose_name='Должность', max_length=10, required=True, choices=POSITIONS)
    wage_rate = db.DecimalField(verbose_name='Ставка', required=True)
    is_active = db.BooleanField(verbose_name='Работает')  # TODO: сделать обязательным, после исправления данных


class Person(db.Document):
    """
    Человек
    Возможно, пользователь системы
    """
    last_name = db.StringField(verbose_name='Фамилия', max_length=32, required=True)
    first_name = db.StringField(verbose_name='Имя', max_length=32, required=True)
    second_name = db.StringField(verbose_name='Отчество', max_length=32)
    emails = db.ListField(db.StringField(max_length=32), verbose_name='Почта')
    degree_history = db.ListField(db.EmbeddedDocumentField(Degree), verbose_name='Уч. степень')
    title_history = db.ListField(db.EmbeddedDocumentField(Title), verbose_name='Уч. звание')
    job_history = db.ListField(db.EmbeddedDocumentField(Job), verbose_name='Должность')
    # TODO: добавить courses_history для ведения истории повышения квалификации

    @property
    def fio(self):
        result = f'{self.last_name} {self.first_name:.1}.'
        if self.second_name:
            result += f'{self.second_name:.1}.'
        return result

    def __str__(self):
        return self.fio


class StudentGroup(db.Document):
    """
    Учебная группа студентов
    TODO: нужно сделать program — справочником
    """
    PROGRAM = (
        ('09.03.01', 'Бак. ИВТ'),
        ('02.03.02', 'Бак. ФИИТ'),
        ('09.04.01', 'Маг. ИВТ'),
        ('02.04.02', 'Маг. ФИИТ'),
    )

    name = db.StringField(verbose_name='Название', max_length=20, required=True)
    program = db.StringField(verbose_name='Программа', max_length=8, required=True, choices=PROGRAM)
    subgroups = db.IntField(verbose_name='Подгруппы', requred=True)
    students = db.IntField(verbose_name='Студенты', requred=True)

    def __str__(self):
        return self.name


class Subject(db.Document):
    """
    Дисциплина
    Может вестись у нескольких групп и идти несколько семестров
    Пока не используется
    """
    name = db.StringField(verbose_name='Название', max_length=100, required=True)


class Course(db.Document):
    """
    Курс для учебной группы в одном семестре
    Если предмет идёт у разных групп — создаем несколько записей
    Если предмет идёт несколько семестров — создаем несколько записей
    Если имеет несколько форм контроля — создаем несколько элементов в списке controls
    """

    CONTROLS = (
        (CT_EXAM, 'Экзамен'),
        (CT_CREDIT_GRADE, 'Зачёт с оценкой'),
        (CT_CREDIT, 'Зачёт'),
        (CT_COURSEWORK, 'Курсовой проект'),
    )

    student_group = db.ReferenceField('StudentGroup', verbose_name='Учеб. группа', required=True, on_delete=CASCADE)
    semester = db.IntField(verbose_name='Семестр', required=True)
    code = db.StringField(verbose_name='Код', max_length=15, required=True)
    name = db.StringField(verbose_name='Название', max_length=100, required=True)

    # Эти поля загружаются из РУП
    hour_lecture = db.IntField(verbose_name='Лекции')        # Лекции
    hour_practice = db.IntField(verbose_name='Практики')     # Практические занятия
    hour_lab_work = db.IntField(verbose_name='Лаб. работы')  # Лабораторные работы
    hour_exam = db.IntField(verbose_name='Часы экз.')        # Экзамен
    hour_homework = db.IntField(verbose_name='СРС')          # СРС
    control = db.IntField(verbose_name='КСР')                # Контроль СР
    controls = db.ListField(db.StringField(max_length=3, choices=CONTROLS), verbose_name='Форма контроля')

    # Эти значения проставляет заведующий кафедрой
    # hour_cons = db.IntField(verbose_name='Предэкз. конс.')   # Предэкзаменационные консультации
    # hour_test = db.IntField(verbose_name='Проверка КР')      # Проверка РГР, рефератов и контрольных работ
    # hour_rating = db.IntField(verbose_name='БРС')            # Ведение БРС
    subject = db.ReferenceField('Subject', verbose_name='Дисциплина', on_delete=NULLIFY)
    teacher = db.ReferenceField('Person', verbose_name='Преподаватель', on_delete=NULLIFY)

    def __str__(self):
        return f'{self.student_group}, {self.semester}: {self.name}'


def get_subjects(rup) -> List[Dict[str, Union[str, Dict[int, Dict[str, int]]]]]:
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


def load_rup(rup, student_group):
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
                old_course_signature = oc.name + str(oc.semester)
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
            course.semester = semester
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
