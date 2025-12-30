from django.db import models
from django.utils import timezone


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

