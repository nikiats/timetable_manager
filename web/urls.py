from django.urls import include, path

import web.views as views

urlpatterns = [
    path('', views.index_view, name='index'),
	path('timetable', views.timetable_view, name='timetable'),
	path('update-timetable', views.update_timetable, name='update_timetable'),
	path('svg-image-available', views.svg_image_available, name='svg_image_available'),
	path('png-image-available', views.png_image_available, name='png_image_available'),

    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout')
]
