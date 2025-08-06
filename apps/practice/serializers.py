from rest_framework import serializers
from django.contrib.auth.models import User
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion
from .models import UserProgress, UserQuestionAttempt


class UserStatsSerializer(serializers.ModelSerializer):
    """Serializer for user statistics."""
    username = serializers.CharField(source='user.username', read_only=True)
    success_rate = serializers.IntegerField(read_only=True)
    average_grade = serializers.FloatField(read_only=True)
    
    class Meta:
        model = UserProgress
        fields = [
            'username',
            'current_level',
            'manual_level',
            'total_questions_attempted',
            'correct_answers_count',
            'success_rate',
            'average_grade',
            'consecutive_high_grades',
            'consecutive_low_grades'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Python programming questions."""
    
    class Meta:
        model = PythonProgrammingQuestion
        fields = [
            'id',
            'instruction',
            'input',
            'output',
            'difficulty_level'
        ]


class CodeSubmissionSerializer(serializers.Serializer):
    """Serializer for code submission."""
    question_id = serializers.IntegerField()
    code = serializers.CharField(allow_blank=True)  # Allow empty code for grade 0
    
    def validate_question_id(self, value):
        if not PythonProgrammingQuestion.objects.filter(id=value).exists():
            raise serializers.ValidationError("Question not found.")
        return value


class CodeExecutionSerializer(serializers.Serializer):
    """Serializer for code execution (without submission)."""
    code = serializers.CharField(allow_blank=True)  # Allow empty code for testing
    test_input = serializers.CharField(required=False, allow_blank=True)


class ManualLevelSerializer(serializers.Serializer):
    """Serializer for setting manual difficulty level."""
    level = serializers.IntegerField(min_value=1, max_value=5)


class LevelChangeSuggestionSerializer(serializers.Serializer):
    """Serializer for level change suggestions."""
    type = serializers.CharField()  # 'level_up' or 'level_down'
    current_level = serializers.IntegerField()
    suggested_level = serializers.IntegerField()
    reason = serializers.CharField()


class GradeFeedbackSerializer(serializers.Serializer):
    """Serializer for grade and feedback response."""
    grade = serializers.IntegerField(min_value=0, max_value=10)
    feedback = serializers.DictField()
    test_results = serializers.DictField()
    execution_time = serializers.FloatField(required=False)
    level_changed = serializers.BooleanField()
    new_level = serializers.IntegerField(required=False)
    level_suggestion = serializers.DictField(required=False)
    
    
class AttemptHistorySerializer(serializers.ModelSerializer):
    """Serializer for attempt history."""
    question_instruction = serializers.CharField(
        source='question.instruction', 
        read_only=True
    )
    
    class Meta:
        model = UserQuestionAttempt
        fields = [
            'id',
            'question_id',
            'question_instruction',
            'submitted_code',
            'grade',
            'execution_time',
            'test_results',
            'feedback',
            'attempted_at'
        ] 