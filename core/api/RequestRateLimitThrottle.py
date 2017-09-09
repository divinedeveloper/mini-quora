from rest_framework import throttling
from core.api.models import User, Question, Answer, Tenant
import datetime
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status

class RequestRateLimitThrottle(throttling.BaseThrottle):

	def wait(self):
		return settings.WAIT_TIME_IN_SECONDS
	
	def allow_request(self, request, view):

		try:
		
			tenant_api_key = request.META.get('HTTP_API_KEY')
			tenant = Tenant.objects.get(api_key = tenant_api_key)

			if tenant.request_date_time is None or datetime.datetime.today().date() != tenant.request_date_time.date():
				tenant.request_date_time = timezone.now()
				tenant.daily_api_requests_count = 0
				tenant.save()

			# #for testing save current datetime
			# tenant.request_date_time = timezone.now()
			# tenant.save()

			if tenant.daily_api_requests_count < settings.REQUESTS_PER_DAY:
				return True
			else:
				timediff =  timezone.now() - tenant.request_date_time
				if timediff.total_seconds() <= settings.WAIT_TIME_IN_SECONDS:
					return False
				else:
					return True

		except Tenant.DoesNotExist as e:
			HttpResponse.status_code = status.HTTP_400_BAD_REQUEST
			return JsonResponse({'status_code': status.HTTP_400_BAD_REQUEST, 'message': "Please provide valid API key"})

	
    	
    	
