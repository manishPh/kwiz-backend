from django.db import models
from django.utils import timezone
from datetime import date, datetime, time
import pytz


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class DailyQuiz(models.Model):
    date = models.DateField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_time = models.TimeField(default="00:00")
    is_released = models.BooleanField(default=False)

    def __str__(self):
        return f"Kwiz {self.date} - {self.category.name}"

    @property
    def is_available(self):
        """Check if quiz is available to play"""
        return self.is_quiz_released()

    def is_quiz_released(self):
        """Check if quiz should be released based on IST timezone"""
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)
        today_ist = now_ist.date()

        # Quiz is available if:
        # 1. Quiz date is today or in the past
        # 2. Quiz is marked as released
        # 3. Current time is past the release time (default midnight IST)
        if self.date > today_ist:
            return False

        if not self.is_released:
            return False

        # If quiz date is in the past, it's available
        if self.date < today_ist:
            return True

        # If quiz date is today, check if release time has passed
        quiz_release_datetime = datetime.combine(self.date, self.release_time)
        quiz_release_datetime_ist = ist.localize(quiz_release_datetime)

        return now_ist >= quiz_release_datetime_ist

    def get_time_until_release(self):
        """Get time remaining until quiz release (in seconds)"""
        if self.is_quiz_released():
            return 0

        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)

        quiz_release_datetime = datetime.combine(self.date, self.release_time)
        quiz_release_datetime_ist = ist.localize(quiz_release_datetime)

        time_diff = quiz_release_datetime_ist - now_ist
        return max(0, int(time_diff.total_seconds()))

    def get_next_quiz_info(self):
        """Get information about the next upcoming quiz"""
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)
        today_ist = now_ist.date()

        # Find next quiz after today
        from django.db.models import Q
        next_quiz = DailyQuiz.objects.filter(
            Q(date__gt=today_ist) |
            Q(date=today_ist, release_time__gt=now_ist.time())
        ).order_by('date', 'release_time').first()

        if next_quiz:
            return {
                'date': next_quiz.date,
                'title': next_quiz.title,
                'category': next_quiz.category.name,
                'time_until_release': next_quiz.get_time_until_release()
            }
        return None

    class Meta:
        verbose_name_plural = "Daily Quizzes"
        ordering = ['-date']


class Question(models.Model):
    quiz = models.ForeignKey(DailyQuiz, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveIntegerField()
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])

    def __str__(self):
        return f"Q{self.order}: {self.text[:50]}..."

    class Meta:
        ordering = ['order']
        unique_together = ['quiz', 'order']


class QuizConfigUpload(models.Model):
    """Model to handle quiz configuration file uploads"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('imported', 'Imported'),
        ('failed', 'Failed'),
    ]

    file = models.FileField(upload_to='quiz_configs/uploads/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    quiz_date = models.DateField(null=True, blank=True)
    quiz_title = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Quiz Config Upload'
        verbose_name_plural = 'Quiz Config Uploads'

    def __str__(self):
        return f"{self.file.name} - {self.status} ({self.uploaded_at.strftime('%Y-%m-%d %H:%M')})"
