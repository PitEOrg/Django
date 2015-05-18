from django.contrib import admin

from .models import Student, Teacher, Subject, SubsubjectType, Subsubject, FinalGrade, Subgrade, SubjectsStudents, SubsubjectsStudents, Message

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(SubsubjectType)
admin.site.register(Subsubject)
admin.site.register(FinalGrade)
admin.site.register(Subgrade)
admin.site.register(SubjectsStudents)
admin.site.register(SubsubjectsStudents)
admin.site.register(Message)

