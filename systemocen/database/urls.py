
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^student/(?P<page_id>[0-9]+)$', views.studentpage, name='studentpage'),
    url(r'^teacher/(?P<page_id>[0-9]+)$', views.teacherpage, name='teacherpage'),
    url(r'^teacher/subject/(?P<subject_id>[0-9]+)$', views.teachersubject, name='teachersubject'),
    url(r'^teacher/subject/(?P<subject_id>[0-9]+)/student/(?P<student_id>[0-9]+)$', views.teacherstudent, name='teacherstudent'),
    url(r'^teacher/deletegrade/$', views.teacherdeletegrade, name='teacherdeletegrade'),
    url(r'^teacher/addgrade/$', views.teacheraddgrade, name='teacheraddgrade'),
    url(r'^student/subject/(?P<subject_id>[0-9]+)$', views.studentsubject, name='studentsubject'),
    url(r'^teacher/subsubject/(?P<subsubject_id>[0-9]+)$', views.teachersubsubject, name='teachersubsubject'),
    url(r'^teacher/subsubject/(?P<subsubject_id>[0-9]+)/student/(?P<student_id>[0-9]+)$', views.subteacherstudent, name='subteacherstudent'),
    url(r'^teacher/deletesubgrade/$', views.teacherdeletesubgrade, name='teacherdeletesubgrade'),
    url(r'^teacher/addsubgrade/$', views.teacheraddsubgrade, name='teacheraddsubgrade'),
    url(r'^student/subsubject/(?P<subsubject_id>[0-9]+)$', views.studentsubsubject, name='studentsubsubject'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)