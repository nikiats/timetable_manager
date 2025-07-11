from django.db import models
from django.contrib.auth.models import User

class Timetable(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	timetable = models.JSONField()


	def count_lessons(self):
		k = 0
		for day in self.timetable:
			for lesson in day:
				k += lesson != '-' and lesson != ''
		return k


	def count_available(self):
		k = 0
		for day in self.timetable:
			for lesson in day:
				k += lesson == '-'
		return k


	def __str__(self):
		lessons = self.count_lessons()
		available = self.count_available()
		return f'<Timetable [lessons: {lessons}, available: {available}]>'

