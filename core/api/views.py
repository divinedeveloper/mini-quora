from django.shortcuts import render

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from core.api.custom_exceptions import CustomApiException
from core.api.services import Services
from rest_framework.decorators import api_view, throttle_classes
from core.api.RequestRateLimitThrottle import RequestRateLimitThrottle
from core.api.serializers import UserSerializer, QuestionSerializer, AnswerSerializer, TenantSerializer 

# Create your views here.

@csrf_exempt
@api_view(['GET'])
@throttle_classes([RequestRateLimitThrottle])
def search_questions(request):
	"""
	search questions based on parameters.
	return Nested Json of Questions with answers and users
	"""

	try: 
		service = Services()

		tenant_api_key = request.META.get('HTTP_API_KEY')

		if tenant_api_key :
			tenant = service.check_valid_api_key(tenant_api_key)
		else:
			raise CustomApiException("Please provide API key", status.HTTP_400_BAD_REQUEST)

		title = request.GET.get('title', None)
		offset = request.GET.get('offset', 0)
		limit = request.GET.get('limit', 10)

		questions, count = service.service_search_questions(title, offset, limit)

		question_serializer = QuestionSerializer(questions, many=True)

		HttpResponse.status_code = status.HTTP_200_OK
		return JsonResponse({'count': count,'questions': question_serializer.data})
	except CustomApiException as err:
		HttpResponse.status_code = err.status_code
		return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	except Exception, e:
		HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})


@csrf_exempt
def dashboard(request):
	"""
	dashboard statistics
	return count of users, questions, answers
	"""

	try: 
		service = Services()

		user_count, question_count, answer_count = service.service_dashboard()

		HttpResponse.status_code = status.HTTP_200_OK
		return JsonResponse({'user_count': user_count,'question_count': question_count, 'answer_count': answer_count})
	except CustomApiException as err:
		HttpResponse.status_code = err.status_code
		return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	except Exception, e:
		HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})


@csrf_exempt
def tenants_dashboard(request):
	"""
	tenants dashboard statistics
	return tenants api request count for all tenants
	"""

	try: 
		service = Services()

		offset = request.GET.get('offset', 0)
		limit = request.GET.get('limit', 10)
		
		tenants, tenants_count = service.service_tenants_dashboard(offset, limit)

		tenants_serializer = TenantSerializer(tenants, many=True)

		HttpResponse.status_code = status.HTTP_200_OK
		return JsonResponse({'count': tenants_count,'tenants': tenants_serializer.data})
	except CustomApiException as err:
		HttpResponse.status_code = err.status_code
		return JsonResponse({'status_code': err.status_code, 'message': err.detail})
	except Exception, e:
		HttpResponse.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return JsonResponse({'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})