from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PythonProgrammingQuestion(models.Model):
    """
    Model to store Python programming questions with their difficulty levels.
    """
    instruction = models.TextField(
        help_text="The programming instruction or question"
    )
    input = models.TextField(
        blank=True,
        help_text="Input example or parameters for the question"
    )
    output = models.TextField(
        help_text="Expected output or solution for the question"
    )
    difficulty_explanation = models.TextField(
        blank=True,
        help_text="Explanation of the difficulty level"
    )
    difficulty_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Difficulty level from 1 (easiest) to 5 (hardest)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'python_programming_questions'
        verbose_name = 'Python Programming Question'
        verbose_name_plural = 'Python Programming Questions'
        indexes = [
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Question (Difficulty: {self.difficulty_level}): {self.instruction[:50]}..." 