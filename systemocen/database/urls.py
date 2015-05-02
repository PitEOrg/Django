from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^student/$', views.studentpage, name='studentpage'),
    url(r'^teacher/$', views.teacherpage, name='teacherpage'),
    url(r'^teacher/subject/(?P<subject_id>[0-9]+)$', views.teachersubject, name='teachersubject'),
    url(r'^student/subject/(?P<subject_id>[0-9]+)$', views.studentsubject, name='studentsubject'),
]

