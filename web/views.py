from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from web.forms import UserLoginForm, UserSignupForm


def index_view(request):
    context = { 'site_name': settings.SITE_NAME }
    print(context)
    return render(request, 'web/index.html', context)


def signup_view(request):
    context = { 'site_name': settings.SITE_NAME }
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)

            return redirect('timetable')
        else:
            context['messages'] = [
                { 'text': 'Ошибка регистрации', 'kind': 'error' }
            ]
            return render(request, 'web/signup.html', context)
    else:
        return render(request, 'web/signup.html', context)


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            pass
            
    context = { 'site_name': settings.SITE_NAME }
    return render(request, 'web/login.html', context)


@login_required
def timetable_view(request):
    context = { 'site_name': settings.SITE_NAME }
    return render(request, 'web/timetable.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')