from django.db.models import (Model, CharField, DateField, DecimalField, FileField, ForeignKey,
                              IntegerField, CASCADE)


class Person(Model):
    last_name = CharField('фамилия', max_length=25)
    first_name = CharField('имя', max_length=25)
    second_name = CharField('отчество', max_length=25, blank=True)

    class Meta:
        abstract = True

    def fio(self):
        result = f'{self.last_name} {self.first_name:.1}.'
        if self.second_name:
            result += f'{self.second_name:.1}.'
        return result

    fio.short_description = 'ФИО'

    def __str__(self):
        return self.fio()


class Teacher(Person):
    DEGREES = (
        ('', 'Без учёной степени'),
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
        ('', 'Без учёного звания'),
        ('доц.', 'Доцент'),
        ('проф.', 'Профессор'),
    )
    degree = CharField('учёная степень', max_length=12, choices=DEGREES, blank=True)
    title = CharField('учёное звание', max_length=5, choices=TITLES, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'second_name']
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'


class Assignment(Model):
    POSITIONS = (
        (0, 'Не работает'),
        (1, 'Ассистент'),
        (2, 'Старший преподаватель'),
        (3, 'Доцент'),
        (4, 'Профессор'),
        (5, 'Заведующий кафедрой'),
    )
    teacher = ForeignKey('Teacher', verbose_name='преподаватель', on_delete=CASCADE)
    position = IntegerField('должность', choices=POSITIONS)
    date = DateField('дата назначения')
    wage_rate = DecimalField('ставка', max_digits=4, decimal_places=2)

    class Meta:
        ordering = ['teacher', 'date']
        verbose_name = 'приём на работу'
        verbose_name_plural = 'приёмы на работу'


class EducationProgram(Model):
    LEVELS = (
        ('B', 'Бакалавриат'),
        ('M', 'Магистратура'),
    )
    level = CharField('уровень', max_length=1, choices=LEVELS)
    code = CharField('код', max_length=8)
    title = CharField('направление', max_length=100)
    subtitle = CharField('профиль', max_length=100, blank=True)
    file = FileField('PLX-файл', upload_to='edu_plan/')

    class Meta:
        ordering = ['level', 'code']
        verbose_name = 'образовательная программа'
        verbose_name_plural = 'образовательные программы'

    def __str__(self):
        return f'{self.code} {self.title}'


class StudyGroup(Model):
    name = CharField('название', max_length=25)
    year = IntegerField('год поступления')
    program = ForeignKey('EducationProgram', verbose_name='образовательная программа', on_delete=CASCADE)

    class Meta:
        ordering = ['program', 'year', 'name']
        verbose_name = 'учебная группа'
        verbose_name_plural = 'учебные группы'

    def __str__(self):
        return self.name


class StudentsNumber(Model):
    study_group = ForeignKey('StudyGroup', verbose_name='учебная группа', on_delete=CASCADE)
    date = DateField('дата изменения')
    subgroups = IntegerField('количество подгрупп')
    students = IntegerField('количество студентов')

    class Meta:
        ordering = ['study_group', 'date']
        verbose_name = 'численность учебной группы'
        verbose_name_plural = 'численность учебных групп'


class Course(Model):
    CONTROLS = (
        ('Эк', 'Экзамен'),
        ('ЗаО', 'Зачёт с оценкой'),
        ('За', 'Зачёт'),
        ('КП', 'Курсовой проект'),
    )
    code = CharField('название', max_length=15)
    name = CharField('название', max_length=50)
    study_group = ForeignKey('StudyGroup', verbose_name='учебная группа', on_delete=CASCADE)
    control = CharField('название', max_length=3, choices=CONTROLS)
    hour_lecture = IntegerField('лек.', blank=0)  # Лекции
    hour_practice = IntegerField('прак.', blank=0)  # Практические занятия
    hour_lab_work = IntegerField('лаб.', blank=0)  # Лабораторные работы
    hour_cons = IntegerField('конс.', blank=0)  # Предэкзаменационные консультации
    hour_exam = IntegerField('экз.', blank=0)  # Экзамен
    hour_test = IntegerField('К.Р.', blank=0)  # Проверка РГР, рефератов и контрольных работ
    hour_home = IntegerField('СРС', blank=0)  # Проверка СРС
    hour_rating = IntegerField('БРС', blank=0)  # Ведение БРС

    class Meta:
        ordering = ['name']
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.name
