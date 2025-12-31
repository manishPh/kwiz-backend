from rest_framework import serializers
from .models import Category, DailyQuiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for quiz questions (without correct answer)"""
    options = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'order', 'text', 'options']
    
    def get_options(self, obj):
        """Return options as a list without revealing correct answer"""
        return [
            obj.option_a,
            obj.option_b,
            obj.option_c,
            obj.option_d,
        ]


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for daily quiz (without answers)"""
    questions = QuestionSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = DailyQuiz
        fields = ['date', 'title', 'description', 'category_name', 'background_image', 'questions']


class QuizResultSerializer(serializers.Serializer):
    """Serializer for quiz submission and results"""
    date = serializers.DateField()
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )


class QuestionResultSerializer(serializers.ModelSerializer):
    """Serializer for question results with correct answers"""
    options = serializers.SerializerMethodField()
    correct_answer = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'order', 'text', 'options', 'correct_answer']
    
    def get_options(self, obj):
        return [
            obj.option_a,
            obj.option_b,
            obj.option_c,
            obj.option_d,
        ]
    
    def get_correct_answer(self, obj):
        """Return the correct answer text"""
        answer_map = {
            'A': obj.option_a,
            'B': obj.option_b,
            'C': obj.option_c,
            'D': obj.option_d,
        }
        return answer_map.get(obj.correct_answer)


class ArchiveQuizSerializer(serializers.ModelSerializer):
    """Serializer for quiz archive listing"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = DailyQuiz
        fields = ['date', 'title', 'category_name', 'is_available']
