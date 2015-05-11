from django.contrib import admin

from .models import Student, Teacher, Subject, Grade, SubjectsStudents, Message

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(SubjectsStudents)
admin.site.register(Message)
