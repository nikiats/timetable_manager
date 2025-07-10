from django.db import models

class Timetable(models.Model):
	lessons = models.JSONField()
