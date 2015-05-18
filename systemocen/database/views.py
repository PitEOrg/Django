from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from .models import Student, Teacher, Subject, SubsubjectType, Subsubject, FinalGrade, Subgrade, SubjectsStudents, SubsubjectsStudents, Message


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
                            return HttpResponseRedirect(reverse('teacherpage', kwargs={'page_id':'0'}))
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
            subjectsStudents = (subjectStudent for subjectStudent in SubjectsStudents.objects.filter(student_id = st))
            subsubjectsStudents = (subsubjectStudent for subsubjectStudent in SubsubjectsStudents.objects.filter(student_id = st))
            subjects = (subjects.subject_id for subjects in st.subjectsstudents_set.all())

            if(request.POST.get('message_id', False)):
                messageToMarkRead = Message.objects.filter(student_id = st).filter(is_read = False).get(pk = request.POST.get('message_id', False))
                messageToMarkRead.is_read = True
                messageToMarkRead.save()    
            messages = Message.objects.filter(student_id = st).filter(is_read = False).order_by('-date')
            allMessages = Message.objects.filter(student_id = st).order_by('-date')
            return render(request, 'database/studentpage.html', {'student': st, 'subjectsStudents': subjectsStudents, 'messages':messages, 'all_messages' : allMessages ,
                                                                 'page_id':page_id, 'subsubjectsStudents' : subsubjectsStudents})
        except Student.DoesNotExist:
            return HttpResponse("Niema studenta")
        except Message.DoesNotExist:
            return HttpResponse("Wiadomosc nie istnieje")
    else:
        return HttpResponse("Nie zalogowany")


def teacherpage(request, page_id):
    if request.user.is_authenticated():
        try:
            te = Teacher.objects.get(user=request.user)
            subjects = (subjects for subjects in te.subject_set.all())
            subSubjects = (subSubjects for subSubjects in te.subsubject_set.all())
            allStudents = Student.objects.all()
            if (request.POST.get('create_message', False) and request.POST.get('student_id', False)):
            	messageTo = Student.objects.get(pk = request.POST.get('student_id', False))
                message = Message(student_id = messageTo, teacher_id = te, contents = request.POST.get('message'), is_read = False, date = timezone.now())
                message.save()
            messages = Message.objects.filter(teacher_id=te).filter(is_read=False).order_by('-date')
            allMessages = Message.objects.filter(teacher_id=te).order_by('-date')

            return render(request, 'database/teacherpage.html',
                          {'teacher': te, 'subjects': subjects, 'messages': messages, 'allMessages': allMessages,
                           'page_id': page_id, 'subSubjects' : subSubjects, 'allStudents' : allStudents})
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")
        except Student.DoesNotExist:
            return HttpResponse("Nie ma studenta")
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


def teachersubsubject(request, subsubject_id):
    if request.user.is_authenticated():
        try:
            te = Teacher.objects.get(user=request.user)
            subsubject = Subsubject.objects.get(pk=subsubject_id)
            if subsubject.teacher_id != te:
                return HttpResponse("Nie prowadzisz tego przedmiotu")
            #students = (subsubjects.student_id for subsubjects in subsubject.subsubjectsstudents_set.all())
            students = (subsubjectStudent.student_id for subsubjectStudent in SubsubjectsStudents.objects.filter(sub_subject_id = subsubject).all())
            return render(request, 'database/teachersubsubject.html', {'teacher': te, 'subsubject': subsubject, 'students': students})
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
                subGrades = (subGrade for subGrade in Subgrade.objects.all().filter(student_id = st).filter(sub_subject_id__subject_id = subject).order_by('-date'))
                subjectsStudents = (subjectStudent for subjectStudent in SubjectsStudents.objects.filter(student_id = st))
            	subsubjectsStudents = (subsubjectStudent for subsubjectStudent in SubsubjectsStudents.objects.filter(student_id = st))
            return render(request, 'database/teacherstudent.html', {'teacher': te, 'subject': subject, 'student': st, 'subGrades': subGrades, 'subjectsStudents':subjectsStudents, 'subsubjectsStudents':subsubjectsStudents})
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


def subteacherstudent(request, subsubject_id, student_id):
    if request.user.is_authenticated():
        try:
            te = Teacher.objects.get(user=request.user)
            subsubject = Subsubject.objects.get(pk=subsubject_id)
            if subsubject.teacher_id != te:
                return HttpResponse("Nie prowadzisz tego przedmiotu")
            subsubjectStudent = SubsubjectsStudents.objects.filter(student_id = student_id).get(sub_subject_id = subsubject_id)
            st = Student.objects.get(pk=student_id)
            if SubjectsStudents.objects.filter(student_id = st.pk).filter(subject_id = subsubject.subject_id):
                subgrades = (subgrade for subgrade in st.subgrade_set.all().filter(sub_subject_id = subsubject.pk))
            return render(request, 'database/subteacherstudent.html', {'teacher': te, 'subsubject': subsubject, 'student': st, 'subgrades': subgrades, 'subsubjectStudent' : subsubjectStudent})
        except Student.DoesNotExist:
            return HttpResponse("Dany student nie istnieje")
        except SubjectsStudents.DoesNotExist:
            return HttpResponse("Student nie jest zapisany na ten przedmiot")
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")

        
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
            term = request.POST['term']
            subject_id = request.POST['subject_id']
            subject_type = request.POST['subject_type']
            st = Student.objects.get(pk = request.POST['student_id'])
            if grade_value != '2.0' and grade_value != '-' and grade_value != '3.0' and grade_value != '3.5' and grade_value != '4.0' and grade_value != '4.5' and grade_value != '5.0':
                return HttpResponse("Zla ocena")
            if term != 'term1' and term != 'term2' and term != 'term3' and term != 'final':
            	return HttpResponse("Zly termin")
            te = Teacher.objects.get(user=request.user)
            if subject_type == 'subject' :
            	subject = Subject.objects.get(pk = subject_id)
            	subjectStudent = SubjectsStudents.objects.get(subject_id = subject, student_id = st)
            	finalGrade = subjectStudent.final_grade_id
            	if term == 'term1' :
            		finalGrade.term1_value = grade_value;
            		finalGrade.term1_date = timezone.now()
            	elif term == 'term2':
            		finalGrade.term2_value = grade_value;
            		finalGrade.term2_date = timezone.now()
            	elif term == 'term3':
            		finalGrade.term3_value = grade_value;
            		finalGrade.term3_date = timezone.now()
            	elif term == 'final':
            		finalGrade.final_value = grade_value;
            		finalGrade.final_date = timezone.now()	
            	finalGrade.save()
            elif subject_type == 'subsubject':
            	subsubject = Subsubject.objects.get(pk = subject_id)
            	subsubjectStudent = SubsubjectsStudents.objects.get(sub_subject_id = subsubject, student_id = st)
            	finalGrade = subsubjectStudent.final_grade_id
            	if term == 'term1' :
            		finalGrade.term1_value = grade_value;
            		finalGrade.term1_date = timezone.now()
            	elif term == 'term2':
            		finalGrade.term2_value = grade_value;
            		finalGrade.term2_date = timezone.now()
            	elif term == 'term3':
            		finalGrade.term3_value = grade_value;
            		finalGrade.term3_date = timezone.now()
            	elif term == 'final':
            		finalGrade.final_value = grade_value;
            		finalGrade.final_date = timezone.now()	
            	finalGrade.save()
     
            
		
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Student.DoesNotExist:
            return HttpResponse("Dany student nie istnieje")
        except SubjectsStudents.DoesNotExist:
            return HttpResponse("Student nie jest zapisany na ten przedmiot")
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")
        except Subject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
        except Subsubject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
            
    else:
        return HttpResponse("Niezalogowany")


def teacherdeletesubgrade(request):
    if request.user.is_authenticated():
        try:
            subgrade = Subgrade.objects.get(pk=request.POST['subgrade_id'])
            te = Teacher.objects.get(user=request.user)
            subsubject = subgrade.sub_subject_id
            if subsubject.teacher_id != te:
                return HttpResponse("Nie prowadzisz tego przedmiotu")
            subgrade.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except SubGrade.DoesNotExist:
            return HttpResponse("Ocena nie istnieje")
        except SubjectsStudents.DoesNotExist:
            return HttpResponse("Student nie jest zapisany na ten przedmiot")
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma nauczyciela")
        except SubSubject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
    else:
        return HttpResponse("Niezalogowany")


def teacheraddsubgrade(request):
    if request.user.is_authenticated():
        try:
            grade_value = request.POST['grade_value']
            if grade_value != '2.0' and grade_value != '2.5' and grade_value != '3.0' and grade_value != '3.5' and grade_value != '4.0' and grade_value != '4.5' and grade_value != '5.0':
                return HttpResponse("Zla ocena")
            te = Teacher.objects.get(user=request.user)
            subsubject = Subsubject.objects.get(pk = request.POST['subsubject_id'])
            if subsubject.teacher_id != te:
                return HttpResponse("Nie prowadzisz tego przedmiotu")
            st = Student.objects.get(pk = request.POST['student_id'])
            if SubjectsStudents.objects.filter(student_id = st.pk).filter(subject_id = subsubject.subject_id.pk):
                subgrade = Subgrade(student_id = st, date = timezone.now(), sub_subject_id = subsubject, value = grade_value, teacher_id = te)
                subgrade.save()
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
            subGrades = (subGrade for subGrade in Subgrade.objects.all().filter(student_id = st).filter(sub_subject_id__subject_id = subject).order_by('-date'))
            return render(request, 'database/studentsubject.html', {'student': st, 'subject': subject, 'subGrades': subGrades})
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma studenta")
        except Subject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
    else:
        return HttpResponse("Niezalogowany")

def studentsubsubject(request, subsubject_id):
    if request.user.is_authenticated():
        try:
            st = Student.objects.get(user=request.user)
            subsubject = SubSubject.objects.get(pk=subsubject_id)
            grades = (grade for grade in st.subgrade_set.all().filter(sub_subject_id=subsubject.pk))
            return render(request, 'database/studentsubject.html', {'student': st, 'subsubject': subsubject, 'grades': grades})
        except Teacher.DoesNotExist:
            return HttpResponse("Nie ma studenta")
        except Subject.DoesNotExist:
            return HttpResponse("Brak przedmiotu")
    else:
        return HttpResponse("Niezalogowany")


def logout_view(request):
    logout(request)
    return render(request, 'database/signin.html')
