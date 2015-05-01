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
		log_step =  request.POST['step']
	except KeyError:
		return render(request, 'database/login.html')
	else:
		if log_step == '1':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('studentpage'))
				else:
					return HttpResponse('Konto wylaczone')
			else:
				return HttpResponse('Bledny login')
		else:
			return HttpResponse('Cos' + log_step)
	return HttpResponse('nic')
	
def testpage(request):
	if request.user.is_authenticated():
		return HttpResponse("Zalogowany")
	else:
		return HttpResponse("Nie zalogowany")
		
def studentpage(request):
	if request.user.is_authenticated():
		try:
			st = Student.objects.get(user = request.user)
			subjects = (subjects.subject_id for subjects in st.subjectsstudents_set.all())
			grades = []
			for grade in st.grade_set.all():
				grades.append([grade.subject_id.name, grade.value])
			
			return render(request, 'database/studentpage.html',{ 'student':st, 'grades':grades, 'subjects':subjects})
		except Student.DoesNotExist:
			return HttpResponse("Niema studenta")
	else:
		return HttpResponse("Nie zalogowany")		
	
	
