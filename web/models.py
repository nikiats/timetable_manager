from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def default_timetable():
	hour_min = getattr(settings, 'DAY_TIME_MIN')
	hour_max = getattr(settings, 'DAY_TIME_MAX')
	
	days = []
	for _ in range(7):
		days.append(['' for _ in range(hour_min, hour_max + 1)])
	
	return days


class Timetable(models.Model):
	lessons = models.JSONField(default=default_timetable())


	def count_lessons(self):
		k = 0
		for day in self.lessons:
			for lesson in day:
				k += lesson != '-' and lesson != ''
		return k


	def count_available(self):
		k = 0
		for day in self.lessons:
			for lesson in day:
				k += lesson == '-'
		return k


	def __str__(self):
		lessons = self.count_lessons()
		available = self.count_available()

		return f'<Timetable [lessons: {lessons}, available: {available}]>'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    timetable = models.OneToOneField(Timetable, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'<Profile username={self.user.username}>'