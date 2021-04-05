from flask_mongoengine import MongoEngine
from mongoengine import CASCADE, NULLIFY

db = MongoEngine()


class Degree(db.EmbeddedDocument):
    DEGREES = (
        ('—', 'Без учёной степени'),
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
    TITLES = (
        ('—', 'Без учёного звания'),
        ('доц.', 'Доцент'),
        ('проф.', 'Профессор'),
    )
    date = db.DateTimeField(verbose_name='Дата')
    title = db.StringField(verbose_name='Уч. звание', max_length=8, choices=TITLES)


class Job(db.EmbeddedDocument):
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


class Person(db.Document):
    last_name = db.StringField(verbose_name='Фамилия', max_length=32, required=True)
    first_name = db.StringField(verbose_name='Имя', max_length=32, required=True)
    second_name = db.StringField(verbose_name='Отчество', max_length=32)
    emails = db.ListField(db.StringField(max_length=32), verbose_name='Почта')
    degree = db.StringField(verbose_name='Уч. степень', max_length=16)
    degree_history = db.ListField(db.EmbeddedDocumentField(Degree), verbose_name='Уч. степень')
    title = db.StringField(verbose_name='Уч. звание', max_length=8)
    title_history = db.ListField(db.EmbeddedDocumentField(Title), verbose_name='Уч. звание')
    job_history = db.ListField(db.EmbeddedDocumentField(Job), verbose_name='Должность')

    @property
    def fio(self):
        result = f'{self.last_name} {self.first_name:.1}.'
        if self.second_name:
            result += f'{self.second_name:.1}.'
        return result

    def __str__(self):
        return self.fio


class JobAssignment(db.Document):
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
        ('—', 'Не работает'),
        ('асс.', 'Ассистент'),
        ('ст.пр.', 'Старший преподаватель'),
        ('доц.', 'Доцент'),
        ('проф.', 'Профессор'),
        ('зав.каф.', 'Заведующий кафедрой'),
    )

    SEMESTERS = (
        ('20-21/1', '2020-21 уч.г., 1 семестр'),
        ('20-21/2', '2020-21 уч.г., 2 семестр'),
    )

    person = db.ReferenceField(Person, verbose_name='Преподаватель', required=True)
    department = db.StringField(verbose_name='Кафедра', max_length=5, required=True, choices=DEPARTMENTS)
    position = db.StringField(verbose_name='Должность', max_length=10, required=True, choices=POSITIONS)
    wage_rate = db.DecimalField(verbose_name='Ставка', required=True)

    def __str__(self):
        result = self.person.fio
        if self.wage_rate == 1:
            result += f', {self.position} каф. {self.department}'
        elif self.wage_rate == 0.5:
            result += f', 0.5 ст. {self.position} каф. {self.department}'
        else:
            result += f', {self.wage_rate:.2f} ст. {self.position} каф. {self.department}'
        return result


class StudentGroup(db.Document):
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


class Course(db.Document):
    CONTROLS = (
        ('Эк', 'Экзамен'),
        ('ЗаО', 'Зачёт с оценкой'),
        ('За', 'Зачёт'),
        ('КП', 'Курсовой проект'),
    )
    code = db.StringField(verbose_name='Код', max_length=15, required=True)
    name = db.StringField(verbose_name='Название', max_length=50, required=True)
    student_group = db.ReferenceField('StudentGroup', verbose_name='Учеб. группа', required=True, on_delete=CASCADE)
    person = db.ReferenceField('Person', verbose_name='Преподаватель', on_delete=NULLIFY)
    control = db.StringField(verbose_name='Контроль', max_length=3, required=True, choices=CONTROLS)
    hour_lecture = db.IntField(verbose_name='Лекции')  # Лекции
    hour_practice = db.IntField(verbose_name='Практики')  # Практические занятия
    hour_lab_work = db.IntField(verbose_name='Лаб. работы')  # Лабораторные работы
    hour_cons = db.IntField(verbose_name='Предэкз. конс.')  # Предэкзаменационные консультации
    hour_exam = db.IntField(verbose_name='Часы экз.')  # Экзамен
    hour_test = db.IntField(verbose_name='Проверка КР')  # Проверка РГР, рефератов и контрольных работ
    hour_home = db.IntField(verbose_name='СРС')  # Проверка СРС
    hour_rating = db.IntField(verbose_name='БРС')  # Ведение БРС

    def __str__(self):
        return self.name
