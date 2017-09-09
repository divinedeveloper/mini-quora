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

# Create your tests here.

@pytest.mark.unittest
class TestUnitViews:

	def setup_method(self):
		"""
		Get instance of APIRequestFactory
		To mock request object which will be directly passed to 
		views as a first argument
		"""
		self.request_factory = APIRequestFactory()
		self.search_questions_api_url = reverse("search_questions")
		self.dashboard_api_url = reverse("dashboard")
		self.tenants_dashboard_api_url = reverse("tenants_dashboard")


	def test_unit_search_questions_blank_title(self, db, django_db_setup, mocker):
		"""
		This method will tests search questions in views
		assert status is 200 and data is returned as per request
		"""

		params = {'title': '', 'offset': '0', 'limit' : '10'}
		request = self.request_factory.get(self.search_questions_api_url, params, HTTP_API_KEY = "6e762d97-2d46-48cc-99b6-58cc0942d514")
		mocker.patch.object(Services, 'service_search_questions')
		mocked_serializer = mocker.patch('core.api.serializers.QuestionSerializer')

		questions = Question.objects.filter(private = False)[params['offset']:params['limit']]
		count = Question.objects.filter(private = False).count()

		Services.service_search_questions.return_value = questions, count
		response = search_questions(request)
		Services.service_search_questions.assert_called_with(params['title'], params['offset'], params['limit'])
		
		mocked_serialize_response = mocked_serializer(questions)
		mocked_serializer.assert_called_with(questions)
		question_serializer = QuestionSerializer(questions, many=True)

		json_response = json.loads(response.content)

		assert response.status_code == status.HTTP_200_OK
		assert json_response['count'] == count
		assert json_response['questions'] != None
		assert json_response['questions'] == question_serializer.data

	
	def test_unit_search_questions_with_title(self, db, django_db_setup, mocker):
		"""
		This method will tests search questions in views
		assert status is 200 and questions are returned
		"""
		params = {'title': 'Sapiente', 'offset': '0', 'limit' : '10'}
		request = self.request_factory.get(self.search_questions_api_url, params, HTTP_API_KEY = "6e762d97-2d46-48cc-99b6-58cc0942d514")
		mocker.patch.object(Services, 'service_search_questions')
		mocked_serializer = mocker.patch('core.api.serializers.QuestionSerializer')

		questions = Question.objects.filter(Q(private = False) & Q(title__icontains = params['title']))[params['offset']:params['limit']]
		count = Question.objects.filter(Q(private = False) & Q(title__icontains = params['title'])).count()

		Services.service_search_questions.return_value = questions, count
		response = search_questions(request)
		Services.service_search_questions.assert_called_with(params['title'], params['offset'], params['limit'])
		
		mocked_serialize_response = mocked_serializer(questions)
		mocked_serializer.assert_called_with(questions)

		json_response = json.loads(response.content)

		question_serializer = QuestionSerializer(questions, many=True)

		assert response.status_code == status.HTTP_200_OK
		assert json_response['count'] == count
		assert json_response['questions'] != None
		assert json_response['questions'] == question_serializer.data

	def test_unit_questions_not_found(self, db, django_db_setup, mocker):
		"""
		This method will tests search questions in views
		assert status is 404 and questions not found message is returned
		"""
		params = {'title': 'myquestion', 'offset': '0', 'limit' : '10'}
		request = self.request_factory.get(self.search_questions_api_url, params, HTTP_API_KEY = "6e762d97-2d46-48cc-99b6-58cc0942d514")

		mock_service_search_questions = mocker.patch.object(Services, 'service_search_questions')
		mock_service_search_questions.side_effect = CustomApiException("Questions not found based on criteria", status.HTTP_404_NOT_FOUND)
		response = search_questions(request)

		Services.service_search_questions.assert_called_with(params['title'], params['offset'], params['limit'])
		json_response = json.loads(response.content)

		assert response.status_code == status.HTTP_404_NOT_FOUND
		assert json_response['message'] == "Questions not found based on criteria"

	def test_unit_dashboard_with_non_zero_counts(self, db, django_db_setup, mocker):
		"""
		This method will tests dashboard in views
		assert status is 200 and counts are returned
		"""
		request = self.request_factory.get(self.dashboard_api_url)
		mocker.patch.object(Services, 'service_dashboard')

		user_count = User.objects.count()
		question_count = Question.objects.count()
		answer_count = Answer.objects.count()

		Services.service_dashboard.return_value = user_count, question_count, answer_count
		response = dashboard(request)
		
		json_response = json.loads(response.content)

		assert Services.service_dashboard.called
		assert response.status_code == status.HTTP_200_OK
		assert json_response['user_count'] == user_count
		assert json_response['question_count'] == question_count
		assert json_response['answer_count'] == answer_count

	def test_unit_dashboard_with_zero_counts_on_blank_db(self, mocker):
		"""
		This method will tests dashboard in views
		assert status is 200 and all 0 counts are returned
		"""
		request = self.request_factory.get(self.dashboard_api_url)
		mocker.patch.object(Services, 'service_dashboard')

		user_count = 0
		question_count = 0
		answer_count = 0

		Services.service_dashboard.return_value = user_count, question_count, answer_count
		response = dashboard(request)
		
		json_response = json.loads(response.content)

		assert Services.service_dashboard.called
		assert response.status_code == status.HTTP_200_OK
		assert json_response['user_count'] == user_count
		assert json_response['question_count'] == question_count
		assert json_response['answer_count'] == answer_count

	def test_unit_tenants_dashboard(self, db, django_db_setup, mocker):
		"""
		This method will tests tenants dashboard in views
		assert status is 200 and tenants with counts are returned
		"""
		params = {'offset': '0', 'limit' : '10'}
		request = self.request_factory.get(self.tenants_dashboard_api_url, params)
		mocker.patch.object(Services, 'service_tenants_dashboard')
		mocked_serializer = mocker.patch('core.api.serializers.TenantSerializer')

		tenants = Tenant.objects.all()[params['offset']:params['limit']]
		tenants_count = Tenant.objects.count()

		Services.service_tenants_dashboard.return_value = tenants, tenants_count
		response = tenants_dashboard(request)

		Services.service_tenants_dashboard.assert_called_with(params['offset'], params['limit'])
		
		mocked_serialize_response = mocked_serializer(tenants)
		mocked_serializer.assert_called_with(tenants)
		tenants_serializer = TenantSerializer(tenants, many=True)
		
		json_response = json.loads(response.content)

		assert response.status_code == status.HTTP_200_OK
		assert json_response['count'] == tenants_count
		assert json_response['tenants'] != None
		assert json_response['tenants'] == tenants_serializer.data

	def test_unit_tenants_dashboard_on_blank_db(self, mocker):
		"""
		This method will tests dashboard in views
		assert status is 200 and counts are returned
		"""
		params = {'offset': '0', 'limit' : '10'}
		request = self.request_factory.get(self.tenants_dashboard_api_url, params)
		mocker.patch.object(Services, 'service_tenants_dashboard')
		mocked_serializer = mocker.patch('core.api.serializers.TenantSerializer')

		tenants = []
		tenants_count = 0

		Services.service_tenants_dashboard.return_value = tenants, tenants_count
		response = tenants_dashboard(request)

		Services.service_tenants_dashboard.assert_called_with(params['offset'], params['limit'])
		
		mocked_serialize_response = mocked_serializer(tenants)
		mocked_serializer.assert_called_with(tenants)
		tenants_serializer = TenantSerializer(tenants, many=True)
		
		json_response = json.loads(response.content)

		assert response.status_code == status.HTTP_200_OK
		assert json_response['count'] == tenants_count
		assert json_response['tenants'] == []
		

	def teardown_method(self):
		self.request_factory = None
		self.search_questions_api_url = None
		self.dashboard_api_url = None
		self.tenants_dashboard_api_url = None
