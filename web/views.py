from django.shortcuts import render
from django.utils import timezone


def get_time_of_day():
    hour = timezone.localtime(timezone.now()).hour
    print(hour)
    if 6 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


def index(request):
    context = { 'greeting': get_time_of_day() }
    return render(request, 'web/index.html', context)


def signup(request):
    return render(request, 'web/signup.html')


def timetable(request):
    return render(request, 'web/timetable.html')