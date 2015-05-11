from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from .models import Student, Teacher, Subject, SubjectsStudents, Grade, Message


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
                        return HttpResponseRedirect(reverse('studentpage',kwargs={'page_id':'0'}))
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


def studentpage(request, page_id):
    if request.user.is_authenticated():
        try:
            st = Student.objects.get(user=request.user)
            subjects = (subjects.subject_id for subjects in st.subjectsstudents_set.all())
            if(request.POST.get('message_id', False)):
                messageToMarkRead = Message.objects.filter(student_id = st).filter(is_read = False).get(pk = request.POST.get('message_id', False))
                messageToMarkRead.is_read = True
                messageToMarkRead.save()    
            messages = Message.objects.filter(student_id = st).filter(is_read = False).order_by('-date')
            allMessages = Message.objects.filter(student_id = st).order_by('-date')
            return render(request, 'database/studentpage.html', {'student': st, 'subjects': subjects, 'messages':messages, 'all_messages' : allMessages ,'page_id':page_id})
        except Student.DoesNotExist:
            return HttpResponse("Niema studenta")
        except Message.DoesNotExist:
            return HttpResponse("Wiadomosc nie istnieje")
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
            if subject.teacher_id != te:
            	return HttpResponse("Nie prowadzisz tego przedmiotu")
            students = (subjects.student_id for subjects in subject.subjectsstudents_set.all())
            return render(request, 'database/teachersubject.html', {'teacher': te, 'subject': subject, 'students': students})
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")
        except Subject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
    else:
        return HttpResponse("Niezalogowany")
        
def teacherstudent(request, subject_id, student_id):
    if request.user.is_authenticated():
        try:
            te = Teacher.objects.get(user=request.user)
            subject = Subject.objects.get(pk=subject_id)
            if subject.teacher_id != te:
            	return HttpResponse("Nie prowadzisz tego przedmiotu")
            st = Student.objects.get(pk=student_id)
            if SubjectsStudents.objects.filter(student_id = st.pk).filter(subject_id = subject.pk):
           	grades = (grade for grade in st.grade_set.all().filter(subject_id = subject.pk))
            	return render(request, 'database/teacherstudent.html', {'teacher': te, 'subject': subject, 'student': st, 'grades': grades})
        except Student.DoesNotExist:
            return HttpResponse("Dany student nie istnieje")
        except SubjectsStudents.DoesNotExist:
            return HttpResponse("Student nie jest zapisany na ten przedmiot")
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")
        except Subject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
    else:
        return HttpResponse("Niezalogowany")
        
def teacherdeletegrade(request):
    if request.user.is_authenticated():
        try:
            grade = Grade.objects.get(pk=request.POST['grade_id'])
            te = Teacher.objects.get(user=request.user)
            subject = grade.subject_id
            if subject.teacher_id != te:
            	return HttpResponse("Nie prowadzisz tego przedmiotu")
            grade.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Grade.DoesNotExist:
            return HttpResponse("Ocena nie istnieje")
        except SubjectsStudents.DoesNotExist:
            return HttpResponse("Student nie jest zapisany na ten przedmiot")
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")
        except Subject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
    else:
        return HttpResponse("Niezalogowany")
        
def teacheraddgrade(request):
    if request.user.is_authenticated():
        try:
            grade_value = request.POST['grade_value']
            if grade_value != '2.0' and grade_value != '2.5' and grade_value != '3.0' and grade_value != '3.5' and grade_value != '4.0' and grade_value != '4.5' and grade_value != '5.0':
            	return HttpResponse("Zla ocena")
            te = Teacher.objects.get(user=request.user)
            subject = Subject.objects.get(pk = request.POST['subject_id'])
            if subject.teacher_id != te:
            	return HttpResponse("Nie prowadzisz tego przedmiotu")
            st = Student.objects.get(pk = request.POST['student_id'])
            if SubjectsStudents.objects.filter(student_id = st.pk).filter(subject_id = subject.pk):
            	gr = Grade(student_id = st, date = timezone.now(), subject_id = subject, value = grade_value, teacher_id = te)
            	gr.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Student.DoesNotExist:
            return HttpResponse("Dany student nie istnieje")
        except SubjectsStudents.DoesNotExist:
            return HttpResponse("Student nie jest zapisany na ten przedmiot")
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
            return HttpResponse("Nie ma studenta")
        except Subject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
    else:
        return HttpResponse("Niezalogowany")
