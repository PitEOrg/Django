from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)

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


class SubSubjectType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SubSubject(models.Model):
    subject_id = models.ForeignKey(Subject)
    teacher_id = models.ForeignKey(Teacher)
    subsubjecttype_id = models.ForeignKey(SubSubjectType, default=0)

    def __str__(self):
        return self.subject_id.name + ' - ' + self.subsubjecttype_id.name


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

    def __str__(self):
        return self.value + ' ' + self.student_id.user.username + ' ' + self.subject_id.name


class SubGrade(models.Model):
    student_id = models.ForeignKey(Student)
    teacher_id = models.ForeignKey(Teacher)
    sub_subject_id = models.ForeignKey(SubSubject)
    value = models.CharField(max_length=3)
    date = models.DateTimeField()

    def __str__(self):
        return self.value + ' ' + self.student_id.user.username + ' ' + self.sub_subject_id.subject_id.name + '-' + self.sub_subject_id.subsubjecttype_id.name


class Message(models.Model):
    student_id = models.ForeignKey(Student)
    teacher_id = models.ForeignKey(Teacher)
    contents = models.CharField(max_length = 400)
    is_read = models.BooleanField()
    date = models.DateTimeField()