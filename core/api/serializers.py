from rest_framework import serializers
from core.api.models import User, Question, Answer, Tenant

class UserSerializer(serializers.ModelSerializer):
	"""
	User serializer for user records
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = User
		fields = '__all__'
		depth = 3


class AnswerSerializer(serializers.ModelSerializer):
	"""
	Answer serializer for answer records
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = Answer
		fields = ('id', 'body', 'user_id')
		depth = 3


class QuestionSerializer(serializers.ModelSerializer):
	"""
	Question serializer for question records
	depth field automatically serializes all fields in nested relations to. 
	"""
	# answers = AnswerSerializer(many=True, read_only=True)
	answers = AnswerSerializer(source='answer_set', many=True)

	class Meta:
		model = Question
		fields = ('id', 'title', 'private', 'user_id', 'answers')
		# fields = '__all__'
		depth = 3


class TenantSerializer(serializers.ModelSerializer):
	"""
	Tenant serializer for tenant records
	depth field automatically serializes all fields in nested relations to. 
	"""
	class Meta:
		model = Tenant
		fields = '__all__'
		depth = 3
