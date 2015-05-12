from django.contrib import admin

from .models import Student, Teacher, Subject, SubSubject, Grade, SubGrade, SubjectsStudents, Message

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(SubSubject)
admin.site.register(Grade)
admin.site.register(SubGrade)
admin.site.register(SubjectsStudents)
admin.site.register(Message)
