from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username


class Subject(models.Model):
    teacher_id = models.ForeignKey(Teacher)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SubjectsStudents(models.Model):
    student_id = models.ForeignKey(Student)
    subject_id = models.ForeignKey(Subject)

    def __str__(self):
        return self.student_id.user.username + ' ' + self.subject_id.name


class Grade(models.Model):
    student_id = models.ForeignKey(Student)
    teacher_id = models.ForeignKey(Teacher)
    subject_id = models.ForeignKey(Subject)
    value = models.CharField(max_length=3)
    date = models.DateTimeField()
    grade_type = models.IntegerField(default=0)

    def __str__(self):
        return self.value + ' ' + self.student_id.user.username + ' ' + self.subject_id.name
	
