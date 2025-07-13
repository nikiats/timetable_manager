from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings

from web.forms import UserLoginForm, UserSignupForm, TimetableCellEditForm
from web.models import Timetable


HOUR_MIN = getattr(settings, 'DAY_TIME_MIN')
MAX_LESSON_LENGTH = getattr(settings, 'MAX_LESSON_LENGTH')
SITE_NAME = getattr(settings, 'SITE_NAME')


def create_error_dicts(form):
    messages = []

    for errors in form.errors.values():
        for error in errors:
            messages.append({ 'text': error, 'kind': 'error' })

    return messages


def index_view(request):
    context = { 
        'site_name': settings.SITE_NAME,
        'authorized': request.user.is_authenticated
    }
    return render(request, 'web/index.html', context)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect(getattr(settings, 'LOGIN_REDIRECT_URL'))

    context = { 'site_name': settings.SITE_NAME }
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                context['messages'] = [{ 'text': 'Пользователь с таким именем уже существует', 'kind': 'error' }]
                return render(request, 'web/signup.html', context)

            user = User.objects.create_user(username=username, password=password)
            Timetable.objects.create(user=user)

            
            login(request, user)
            return redirect('web:timetable')
        else:
            context['messages'] = create_error_dicts(form)
            return render(request, 'web/signup.html', context)
    else:
        return render(request, 'web/signup.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect(getattr(settings, 'LOGIN_REDIRECT_URL'))

    context = { 'site_name': settings.SITE_NAME }
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('web:timetable')
            else:
                context['messages'] = [{ 'text': 'Некорректные данные для входа', 'kind': 'error' }]
        else:
            context['messages'] = create_error_dicts(form)

    return render(request, 'web/login.html', context)


@login_required
def timetable_view(request):
    timetable = request.user.timetable
    table_content = timetable.to_rows()
    context = { 
        'max_lesson_length': MAX_LESSON_LENGTH,
        'site_name': SITE_NAME,
        'timetable': table_content
    }
    return render(request, 'web/timetable.html', context)


def logout_view(request):
    logout(request)
    return redirect('web:index')


@login_required
def update_timetable(request):
    if request.method == 'POST':
        form = TimetableCellEditForm(request.POST)
        if form.is_valid():
            timetable = request.user.timetable

            day_index = form.cleaned_data['day_index']
            hour = form.cleaned_data['hour']

            timetable.contents[day_index][hour - HOUR_MIN] = form.cleaned_data['value']
            timetable.save()
            return JsonResponse({'success': True, 'errors': []}, status=200)
        else:
            return JsonResponse({ 'success': False, 'errors': list(form.errors.items()) }, status=400)