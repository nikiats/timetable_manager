from django.conf import settings


HOUR_MIN = getattr(settings, 'DAY_TIME_MIN')
HOUR_MAX = getattr(settings, 'DAY_TIME_MAX')

CELLS_X = [100, 250, 400, 550, 700, 850, 1000] # Столбцы с днями недели
CELLS_Y = [
    40,   # 7:00
    70,   # 8:00
    100,  # 9:00
    130,  # 10:00
    160,  # 11:00
    190,  # 12:00
    220,  # 13:00
    250,  # 14:00
    280,  # 15:00
    310,  # 16:00
    340,  # 17:00
    370,  # 18:00
    400,  # 19:00
    430,  # 20:00
    460,  # 21:00
    490,  # 22:00
    520   # 23:00
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