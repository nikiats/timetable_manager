from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


HOUR_MIN = getattr(settings, 'DAY_TIME_MIN')
HOUR_MAX = getattr(settings, 'DAY_TIME_MAX')


def default_lessons():
	days = []
	for _ in range(7):
		days.append(['' for _ in range(HOUR_MIN, HOUR_MAX + 1)])
	
	return days


class Timetable(models.Model):
	user = models.OneToOneField(
		User,
		related_name='timetable',
		on_delete=models.CASCADE
	)
	contents = models.JSONField(default=default_lessons())


	def count_lessons(self):
		k = 0
		for day in self.contents:
			for lesson in day:
				k += lesson != '-' and lesson != ''
		return k


	def count_available(self):
		k = 0
		for day in self.contents:
			for lesson in day:
				k += lesson == '-'
		return k


	def to_table(self):
		rows = [{ 'hour': str(hour) + ':00', 'lessons': [] } for hour in range(HOUR_MIN, HOUR_MAX + 1)]
		for day in self.contents:
			for i, lesson in enumerate(day):
				rows[i]['lessons'].append(lesson)
		return rows


	def __str__(self):
		lessons = self.count_lessons()
		available = self.count_available()

		return f'<Timetable [lessons: {lessons}, available: {available}]>'


# class Profile(models.Model):
#     user = models.OneToOneField(
# 		User,
# 		on_delete=models.CASCADE,
# 		null=False,
# 		related_name='profile'
# 	)

#     timetable = models.OneToOneField(
# 		Timetable,
# 		on_delete=models.CASCADE,
# 		null=False,
# 		related_name='profile'
# 	)

#     def __str__(self):
#         return f'<Profile username={self.user.username}>'
