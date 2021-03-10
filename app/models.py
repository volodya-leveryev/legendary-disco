from django.db.models import (Model, BooleanField, CharField, DateField, ForeignKey, IntegerField, DecimalField,
                              TextField, CASCADE)


class Person(Model):
    last_name = CharField('фамилия', max_length=25)
    first_name = CharField('имя', max_length=25)
    second_name = CharField('отчество', max_length=25, blank=True)

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name', 'second_name']

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


class StudyGroup(Model):
    name = CharField('название', max_length=25)
    year = IntegerField('год поступления')

    class Meta:
        verbose_name = 'учебная группа'
        verbose_name_plural = 'учебные группы'

    def __str__(self):
        return self.name


class Student(Person):
    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'


class Admission(Model):
    student = ForeignKey('Student', verbose_name='студент', on_delete=CASCADE)
    study_group = ForeignKey('StudyGroup', verbose_name='учебная группа', on_delete=CASCADE)
    is_studying = BooleanField('обучается')
    comment = TextField('комментарий', blank=True)

    class Meta:
        verbose_name = 'зачисление'
        verbose_name_plural = 'зачисления'


class Course(Model):
    name = CharField('название', max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
        return self.name
