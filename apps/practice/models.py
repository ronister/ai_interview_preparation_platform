from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.instructions_difficulty_eval.models import PythonProgrammingQuestion


class UserProgress(models.Model):
    """
    Tracks user's progress through the coding challenges.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='practice_progress'
    )
    current_level = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Current difficulty level (1-5)"
    )
    manual_level = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="User's manually set difficulty level preference (1-5)"
    )
    current_question = models.ForeignKey(
        PythonProgrammingQuestion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_for_users',
        help_text="The question currently assigned to the user"
    )
    question_assigned_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the current question was assigned"
    )
    consecutive_high_grades = models.IntegerField(
        default=0,
        help_text="Number of consecutive grades 7-10"
    )
    consecutive_low_grades = models.IntegerField(
        default=0,
        help_text="Number of consecutive grades 0-3"
    )
    total_questions_attempted = models.IntegerField(
        default=0,
        help_text="Total number of questions attempted"
    )
    correct_answers_count = models.IntegerField(
        default=0,
        help_text="Number of correct answers (grades 7-10)"
    )
    total_score = models.IntegerField(
        default=0,
        help_text="Sum of all grades received"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progress'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['current_level']),
            models.Index(fields=['manual_level']),
            models.Index(fields=['current_question']),
        ]

    def __str__(self):
        return f"{self.user.username} - Level {self.current_level} (Manual: {self.manual_level})"

    @property
    def success_rate(self):
        """Calculate success rate as percentage of correct answers (grades 7-10)."""
        if self.total_questions_attempted == 0:
            return 0
        return round((self.correct_answers_count / self.total_questions_attempted) * 100)

    @property
    def average_grade(self):
        """Calculate average grade as total_score / total_questions_attempted."""
        if self.total_questions_attempted == 0:
            return 0.0
        return round(self.total_score / self.total_questions_attempted, 1)

    def assign_question(self, question):
        """Assign a new question to the user."""
        from django.utils import timezone
        self.current_question = question
        self.question_assigned_at = timezone.now()
        self.save()

    def clear_current_question(self):
        """Clear the current question after submission."""
        self.current_question = None
        self.question_assigned_at = None
        self.save()

    def update_level(self, new_grade):
        """Update user level based on new grade."""
        if new_grade >= 7:
            self.consecutive_high_grades += 1
            self.consecutive_low_grades = 0
            if self.consecutive_high_grades >= 3 and self.current_level < 5:
                self.current_level += 1
                self.consecutive_high_grades = 0
        elif new_grade <= 3:  # This includes grade 0
            self.consecutive_low_grades += 1
            self.consecutive_high_grades = 0
            if self.consecutive_low_grades >= 3 and self.current_level > 1:
                self.current_level -= 1
                self.consecutive_low_grades = 0
        else:
            # Grade 4-6: reset both counters
            self.consecutive_high_grades = 0
            self.consecutive_low_grades = 0
        
        self.save()

    def check_level_change_suggestion(self, new_grade):
        """Check if user should be prompted for level change based on consecutive grades."""
        suggestion = None
        
        if new_grade >= 7:
            new_consecutive_high = self.consecutive_high_grades + 1
            if new_consecutive_high >= 3 and self.manual_level < 5:
                suggestion = {
                    'type': 'level_up',
                    'current_level': self.manual_level,
                    'suggested_level': self.manual_level + 1,
                    'reason': 'You have 3 consecutive high grades (7+)! Consider increasing difficulty.'
                }
        elif new_grade <= 3:
            new_consecutive_low = self.consecutive_low_grades + 1
            if new_consecutive_low >= 3 and self.manual_level > 1:
                suggestion = {
                    'type': 'level_down',
                    'current_level': self.manual_level,
                    'suggested_level': self.manual_level - 1,
                    'reason': 'You have 3 consecutive low grades (3-). Consider decreasing difficulty.'
                }
        
        return suggestion

    def set_manual_level(self, level):
        """Set the user's manual level preference."""
        if 1 <= level <= 5:
            self.manual_level = level
            # Reset consecutive grades counters when user manually sets level
            self.consecutive_high_grades = 0
            self.consecutive_low_grades = 0
            self.save()
            return True
        return False

    def get_effective_level(self):
        """Get the level to use for next question (manual level takes precedence)."""
        return self.manual_level


class UserQuestionAttempt(models.Model):
    """
    Records each attempt a user makes at solving a question.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='question_attempts'
    )
    question = models.ForeignKey(
        PythonProgrammingQuestion,
        on_delete=models.CASCADE,
        related_name='user_attempts'
    )
    submitted_code = models.TextField(
        help_text="The code submitted by the user"
    )
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Grade received (0-10, where 0 is for empty/comments-only code)"
    )
    execution_time = models.FloatField(
        null=True,
        blank=True,
        help_text="Code execution time in seconds"
    )
    test_results = models.JSONField(
        default=dict,
        help_text="Detailed test case results"
    )
    feedback = models.JSONField(
        default=dict,
        help_text="Detailed feedback on the submission"
    )
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Question Attempt'
        verbose_name_plural = 'User Question Attempts'
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['user', 'question']),
            models.Index(fields=['attempted_at']),
            models.Index(fields=['grade']),
        ]

    def __str__(self):
        return f"{self.user.username} - Question {self.question.id} - Grade: {self.grade}"
