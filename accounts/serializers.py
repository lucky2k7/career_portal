from rest_framework import serializers
from .models import Question, Option, UserAnswer

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Option
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(source='option_set', many=True)
    class Meta:
        model=Question
        fields = ['id', 'text', 'options']

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['question', 'selected_option']