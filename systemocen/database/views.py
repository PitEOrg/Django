from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from .models import Student, Teacher, Subject, SubjectsStudents


def index(request):
    return render(request, 'database/index.html')


def signin(request):
    try:
        log_step = request.POST['step']
    except KeyError:
        return render(request, 'database/signin.html')
    else:
        if log_step == '1':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    try:
                        student = Student.objects.get(user=request.user)
                        return HttpResponseRedirect(reverse('studentpage'))
                    except Student.DoesNotExist:
                        try:
                            teacher = Teacher.objects.get(user=request.user)
                            return HttpResponseRedirect(reverse('teacherpage'))
                        except Teacher.DoesNotExist:
                            return HttpResponse('Konto nie prydzielone')
                else:
                    return HttpResponse('Konto wylaczone')
            else:
                return HttpResponse('Bledny login')
        else:
            return HttpResponse('Cos' + log_step)


def testpage(request):
    if request.user.is_authenticated():
        return HttpResponse("Zalogowany")
    else:
        return HttpResponse("Nie zalogowany")


def studentpage(request):
    if request.user.is_authenticated():
        try:
            st = Student.objects.get(user=request.user)
            subjects = (subjects.subject_id for subjects in st.subjectsstudents_set.all())
            return render(request, 'database/studentpage.html', {'student': st, 'subjects': subjects})
        except Student.DoesNotExist:
            return HttpResponse("Niema studenta")
    else:
        return HttpResponse("Nie zalogowany")


def teacherpage(request):
    if request.user.is_authenticated():
        try:
            te = Teacher.objects.get(user=request.user)
            subjects = (subjects for subjects in te.subject_set.all())
            return render(request, 'database/teacherpage.html', {'teacher': te, 'subjects': subjects})
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")
    else:
        return HttpResponse("Niezalogowany")


def teachersubject(request, subject_id):
    if request.user.is_authenticated():
        try:
            te = Teacher.objects.get(user=request.user)
            subject = Subject.objects.get(pk=subject_id)
            students = (subjects.student_id for subjects in subject.subjectsstudents_set.all())
            return render(request, 'database/teachersubject.html', {'teacher': te, 'subject': subject, 'students': students})
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")
        except Subject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
    else:
        return HttpResponse("Niezalogowany")

def studentsubject(request, subject_id):
    if request.user.is_authenticated():
        try:
            st = Student.objects.get(user=request.user)
            subject = Subject.objects.get(pk=subject_id)
            grades = (grade for grade in st.grade_set.all().filter(subject_id=subject.pk))
            return render(request, 'database/studentsubject.html', {'student': st, 'subject': subject, 'grades': grades})
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")
        except Subject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
    else:
        return HttpResponse("Niezalogowany")