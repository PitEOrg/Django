from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='student_profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='teacher_profile_images', blank=True)
	
    def __str__(self):
        return self.user.username


class Subject(models.Model):
    teacher_id = models.ForeignKey(Teacher)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class SubsubjectType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Subsubject(models.Model):
    subject_id = models.ForeignKey(Subject)
    teacher_id = models.ForeignKey(Teacher)
    subsubjecttype_id = models.ForeignKey(SubsubjectType)

    def __str__(self):
        return self.subject_id.name + ' (' + self.subsubjecttype_id.name + ') - ' + self.teacher_id.user.first_name + ' ' + self.teacher_id.user.last_name
        
        
class FinalGrade(models.Model):
    student_id = models.ForeignKey(Student)
    subsubject_id = models.ForeignKey(Subsubject)
    final_value = models.CharField(max_length=3, default='-')
    final_date = models.DateTimeField()
    term1_value = models.CharField(max_length=3, default='-')
    term1_date = models.DateTimeField()
    term2_value = models.CharField(max_length=3, default='-')
    term2_date = models.DateTimeField()
    term3_value = models.CharField(max_length=3, default='-')
    term3_date = models.DateTimeField()
    
    def __str__(self):
        return self.subsubject_id.subject_id.name + ' ( ' + self.subsubject_id.subsubjecttype_id.name + ' ) ' + self.student_id.user.first_name + ' ' + self.student_id.user.last_name



class Subgrade(models.Model):
    student_id = models.ForeignKey(Student)
    teacher_id = models.ForeignKey(Teacher)
    sub_subject_id = models.ForeignKey(Subsubject)
    value = models.CharField(max_length=3)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value + ' ' + self.student_id.user.username + ' ' + self.sub_subject_id.subject_id.name + '-' + self.sub_subject_id.subsubjecttype_id.name



class SubjectsStudents(models.Model):
    student_id = models.ForeignKey(Student)
    subject_id = models.ForeignKey(Subject)
    final_grade_id = models.OneToOneField(FinalGrade)
    def __str__(self):
        return self.student_id.user.username + ' ' + self.subject_id.name
        
        
class SubsubjectsStudents(models.Model):
    student_id = models.ForeignKey(Student)
    sub_subject_id = models.ForeignKey(Subsubject)
    final_grade_id = models.OneToOneField(FinalGrade)


    def __str__(self):
        return self.student_id.user.username 

class Message(models.Model):
    student_id = models.ForeignKey(Student)
    teacher_id = models.ForeignKey(Teacher)
    contents = models.CharField(max_length = 400)
    is_read = models.BooleanField()
    date = models.DateTimeField()
