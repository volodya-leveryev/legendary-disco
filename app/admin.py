from django.contrib import admin

from .models import Course, StudentGroup, Teacher, Position


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('fio', 'degree', 'title')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'position', 'wage_rate', 'date')
