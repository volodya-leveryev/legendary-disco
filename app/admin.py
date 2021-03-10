from django.contrib import admin

from .models import (Course, StudyGroup, Teacher, Assignment, Student, Admission)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('fio', 'degree', 'title')


@admin.register(Assignment)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'position', 'wage_rate', 'date')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('fio',)


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'study_group', 'is_studying')
