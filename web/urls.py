from django.urls import include, path

import web.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
	path('account', include('django.contrib.auth.urls')),
	path('timetable', views.timetable, name='timetable')
]