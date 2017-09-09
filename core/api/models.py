from django.db import models
from django.utils import timezone
import datetime
import uuid

# Create your models here.
class User(models.Model):
	name = models.CharField(blank = False, max_length = 50)

class Question(models.Model):
	title = models.CharField(blank = False, max_length = 100)
	private = models.BooleanField(blank=True)
	user_id = models.ForeignKey(User)

class Answer(models.Model):
	body = models.TextField(blank = False)
	question_id = models.ForeignKey(Question)
	user_id = models.ForeignKey(User)

class Tenant(models.Model):
	name = models.CharField(blank = False, max_length = 20)
	api_key = models.UUIDField(default = uuid.uuid4, editable = False)
	api_requests_count = models.PositiveSmallIntegerField(blank = False)
	request_date_time = models.DateTimeField()
	daily_api_requests_count = models.PositiveSmallIntegerField(blank = False)





