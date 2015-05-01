from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.signin, name='signin'),
	url(r'^testpage/$', views.testpage, name='testpage'),
	url(r'^studentpage/$',views.studentpage, name='studentpage'),
]

