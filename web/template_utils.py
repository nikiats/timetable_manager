from django.conf import settings


HOUR_MIN = getattr(settings, 'DAY_TIME_MIN')
HOUR_MAX = getattr(settings, 'DAY_TIME_MAX')

CELLS_X = [100, 250, 400, 550, 700, 850, 1000]
CELLS_Y = [
    40,
    70,
    100,
    130,
    160,
    190,
    220,
    250,
    280,
    310,
    340,
    370,
    400,
    430,
    460,
    490,
    520 
]


def template_hours():
    """
    Данные о часах для шаблонизатора таблицы с доступным временем
    """
    return [
        { 
            'hour': hour,
            'y': CELLS_Y[i]
        } 
        for i, hour in enumerate(range(HOUR_MIN, HOUR_MAX + 1))
    ]


def template_available_data(timetable_content):
    """
    Подготовка данных о занятиях для шаблонизатора таблицы с доступным временем
    """
    days = []

    for i, day in enumerate(timetable_content):
        lessons = []
        for j, lesson in enumerate(day):
            lessons.append({ 'y': CELLS_Y[j], 'content': lesson })

        days.append({ 'x': CELLS_X[i], 'lessons': lessons })

    hours = template_hours()
    return days, hours