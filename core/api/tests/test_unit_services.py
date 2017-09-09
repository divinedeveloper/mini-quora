from rest_framework.test import APIRequestFactory, APIClient
from rest_framework import status
from django.conf import settings
from core.api.models import User, Question, Answer, Tenant
from core.api.custom_exceptions import CustomApiException
from core.api.services import Services 
from core.api.serializers import UserSerializer, QuestionSerializer, AnswerSerializer, TenantSerializer 
from core.api.views import search_questions, dashboard, tenants_dashboard
from django.core.urlresolvers import reverse
from django.db.models import Q
import pytest
from pytest_mock import mocker
from django.core.management import call_command
import json

@pytest.mark.unittest
class TestUnitServices:

	def setup_method(self):
		"""
		Initial setup
		"""
		self.title = None
		self.offset = 0
		self.limit = 10
		self.service_instance = Services()

	def test_unit_search_question_blank_title(self, db, django_db_setup, mocker):

		questions_list = Question.objects.filter(private = False)[self.offset : self.limit]
		count = Question.objects.filter(private = False).count()

		result_questions_list, result_count = self.service_instance.service_search_questions(None, self.offset, self.limit)

		assert count == result_count

	def test_unit_search_question_with_title(self, db, django_db_setup, mocker):

		questions_list = Question.objects.filter(Q(private = False) & Q(title__icontains = 'Quod labore'))[self.offset : self.limit]
		count = Question.objects.filter(Q(private = False) & Q(title__icontains = 'Quod labore')).count()

		result_questions_list, result_count = self.service_instance.service_search_questions('Quod labore', self.offset, self.limit)

		assert count == result_count

	def test_unit_search_question_not_found(self, db, django_db_setup, mocker):

		questions_list = Question.objects.filter(Q(private = False) & Q(title__icontains = 'My Question'))[self.offset : self.limit]
		count = Question.objects.filter(Q(private = False) & Q(title__icontains = 'My Question')).count()

		with pytest.raises(CustomApiException) as exc_info:
			CustomApiException("Questions not found based on criteria", status.HTTP_404_NOT_FOUND)

			self.service_instance.service_search_questions('My Question', self.offset, self.limit)


	def test_unit_check_valid_api_key_succes_case(self, db, django_db_setup, mocker):

		tenant = Tenant.objects.get(api_key = "18ca9a9b-50f3-47e5-bb77-cee5575060d0")
		old_api_request_count = tenant.api_requests_count

		self.service_instance.check_valid_api_key(tenant.api_key)

		post_saving_tenant = Tenant.objects.get(api_key = tenant.api_key)

		assert post_saving_tenant.api_requests_count == old_api_request_count + 1

	def test_unit_check_valid_api_key_error_case(self, db, django_db_setup, mocker):

		with pytest.raises(CustomApiException) as exc_info:
			CustomApiException("Please provide valid API key", status.HTTP_400_BAD_REQUEST)

			self.service_instance.check_valid_api_key("20ca9a9b-50f3-47e5-bb77-cee5575060d0")

	def test_unit_service_dashboard(self, db, django_db_setup, mocker):

		check_user_count = User.objects.count()
		check_question_count = Question.objects.count()
		check_answer_count = Answer.objects.count()

		user_count, question_count, answer_count = self.service_instance.service_dashboard()

		assert user_count == check_user_count
		assert question_count == check_question_count
		assert answer_count == check_answer_count

	def test_unit_service_tenants_dashboard(self, db, django_db_setup, mocker):

		check_tenants_list = Tenant.objects.all()[self.offset : self.limit]
		check_tenants_count = Tenant.objects.count()

		tenants, tenants_count = self.service_instance.service_tenants_dashboard(self.offset, self.limit)

		assert check_tenants_count == tenants_count
		assert tenants != [] or None


	def teardown_method(self):
		"""
		Set values to none
		"""
		self.title = None
		self.offset = None
		self.limit = None
		self.service_instance = None
