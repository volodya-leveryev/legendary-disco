from django.contrib import admin

from .models import (Teacher, Assignment, EducationProgram, StudyGroup, StudentsNumber, Course)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('fio', 'degree', 'title')


@admin.register(Assignment)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'position', 'wage_rate', 'date')


@admin.register(EducationProgram)
class EducationProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'level')


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'program')


@admin.register(StudentsNumber)
class StudentsNumberAdmin(admin.ModelAdmin):
    list_display = ('study_group', 'date', 'subgroups', 'students')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('study_group', 'name',)
