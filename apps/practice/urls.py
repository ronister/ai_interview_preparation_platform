from django.urls import path
from . import views

app_name = 'practice'

urlpatterns = [
    path('user-stats/', views.get_user_stats, name='user-stats'),
    path('set-manual-level/', views.set_manual_level, name='set-manual-level'),
    path('next-question/', views.get_next_question, name='next-question'),
    path('run-python/', views.run_python_code, name='run-python'),  # New backend Python execution
    path('submit-solution/', views.submit_solution, name='submit-solution'),
    path('abandon-question/', views.abandon_current_question, name='abandon-question'),
    path('attempt-history/', views.get_attempt_history, name='attempt-history'),
    path('clear-progress/', views.clear_user_progress, name='clear-progress'),
] 