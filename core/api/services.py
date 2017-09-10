from django.db import transaction
from django.conf import settings
from core.api.models import User, Question, Answer, Tenant
from core.api.custom_exceptions import CustomApiException
from rest_framework import status
from django.db.models import Q
import json
from django.utils import timezone
from uuid import UUID

class Services():
	def __init__(self):
		return


	def validate_uuid4(self, api_key):
		try:
			val = UUID(api_key, version=4)
		except:
			raise CustomApiException("Tenant API key is not valid UUID", status.HTTP_400_BAD_REQUEST)

		return val.hex == api_key.replace('-', '')



	def service_search_questions(self, title, offset, limit):
		#depending on the parameters fire query and get results
		#based on pagination

		questions_list = []
		count = 0

		if not title:
			questions_list = Question.objects.filter(private = False)[offset:limit]
			count = Question.objects.filter(private = False).count()

		if title:
			questions_list = Question.objects.filter(Q(private = False) & Q(title__icontains = title))[offset:limit]
			count = Question.objects.filter(Q(private = False) & Q(title__icontains = title)).count()

		if not questions_list:
			raise CustomApiException("Questions not found based on criteria", status.HTTP_404_NOT_FOUND)

		return questions_list, count


	@transaction.atomic
	def check_valid_api_key(self, api_key):
		try:
			tenant = Tenant.objects.get(api_key = api_key)
			tenant.api_requests_count += 1
			tenant.request_date_time = timezone.now()
			tenant.daily_api_requests_count += 1
			tenant.save()
			return tenant
		except Tenant.DoesNotExist as e:
			raise CustomApiException("Please provide valid API key", status.HTTP_400_BAD_REQUEST)


	def service_dashboard(self):
		user_count = 0
		question_count = 0
		answer_count = 0

		user_count = User.objects.count()
		question_count = Question.objects.count()
		answer_count = Answer.objects.count()

		return user_count, question_count, answer_count

	def service_tenants_dashboard(self, offset, limit):
		tenants = []
		tenants_count = 0

		tenants = Tenant.objects.all()[offset:limit]
		tenants_count = Tenant.objects.count()

		return tenants, tenants_count

