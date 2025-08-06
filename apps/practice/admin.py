from django.contrib import admin
from .models import UserProgress, UserQuestionAttempt


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_level', 'total_questions_attempted', 'success_rate', 'updated_at']
    list_filter = ['current_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['success_rate', 'created_at', 'updated_at']


@admin.register(UserQuestionAttempt)
class UserQuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'grade', 'attempted_at']
    list_filter = ['grade', 'attempted_at']
    search_fields = ['user__username', 'question__instruction']
    readonly_fields = ['attempted_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'question')
