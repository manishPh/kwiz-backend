from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from .models import Category, DailyQuiz, Question, QuizConfigUpload
import json
from datetime import datetime
from kwiz_project.constants import (
    REQUIRED_QUIZ_FIELDS, REQUIRED_QUESTION_FIELDS,
    REQUIRED_OPTIONS_COUNT, VALID_ANSWER_INDICES,
    ANSWER_CHOICES, DATE_FORMAT,
    ERROR_QUIZ_ALREADY_EXISTS, ERROR_MISSING_FIELD,
    ERROR_INVALID_QUESTIONS, ERROR_NO_QUESTIONS,
    ERROR_INVALID_OPTIONS_COUNT, ERROR_INVALID_CORRECT_ANSWER,
    DEFAULT_CATEGORY_DESCRIPTION_TEMPLATE,
    SUCCESS_QUIZ_IMPORTED
)


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['order', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(DailyQuiz)
class DailyQuizAdmin(admin.ModelAdmin):
    list_display = ['date', 'title', 'category', 'is_released', 'is_available']
    list_filter = ['category', 'is_released', 'date']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'
    inlines = [QuestionInline]

    def is_available(self, obj):
        return obj.is_available
    is_available.boolean = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'order', 'text', 'correct_answer']
    list_filter = ['quiz__category', 'correct_answer']
    search_fields = ['text']


@admin.register(QuizConfigUpload)
class QuizConfigUploadAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'quiz_title', 'quiz_date', 'status', 'uploaded_at', 'uploaded_by']
    list_filter = ['status', 'uploaded_at']
    search_fields = ['quiz_title', 'uploaded_by']
    readonly_fields = ['uploaded_at', 'status', 'error_message', 'quiz_date', 'quiz_title', 'status_display']
    actions = ['import_quiz_configs']

    fieldsets = (
        ('Upload', {
            'fields': ('file', 'uploaded_by')
        }),
        ('Status', {
            'fields': ('status_display', 'uploaded_at', 'quiz_date', 'quiz_title', 'error_message')
        }),
    )

    def file_name(self, obj):
        return obj.file.name.split('/')[-1] if obj.file else '-'
    file_name.short_description = 'File Name'

    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'imported': 'green',
            'failed': 'red',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_display.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        """Auto-import quiz when file is uploaded"""
        if not change:  # Only on create
            obj.uploaded_by = request.user.username
        super().save_model(request, obj, form, change)

        # Auto-import if status is pending
        if obj.status == 'pending':
            self.import_single_config(request, obj)

    def import_quiz_configs(self, request, queryset):
        """Admin action to import selected quiz configs"""
        success_count = 0
        fail_count = 0

        for upload in queryset.filter(status='pending'):
            if self.import_single_config(request, upload):
                success_count += 1
            else:
                fail_count += 1

        if success_count:
            self.message_user(
                request,
                f'Successfully imported {success_count} quiz config(s)',
                messages.SUCCESS
            )
        if fail_count:
            self.message_user(
                request,
                f'Failed to import {fail_count} quiz config(s)',
                messages.ERROR
            )

    import_quiz_configs.short_description = 'Import selected quiz configs'

    def import_single_config(self, request, upload):
        """Import a single quiz config"""
        try:
            # Read and parse JSON file
            upload.file.seek(0)
            config = json.load(upload.file)

            # Validate configuration
            self.validate_config(config)

            # Extract quiz info
            quiz_date = datetime.strptime(config['date'], DATE_FORMAT).date()
            upload.quiz_date = quiz_date
            upload.quiz_title = config['title']

            # Check if quiz already exists
            if DailyQuiz.objects.filter(date=quiz_date).exists():
                raise ValueError(ERROR_QUIZ_ALREADY_EXISTS.format(date=quiz_date))

            # Get or create category
            category, _ = Category.objects.get_or_create(
                name=config['category'],
                defaults={'description': DEFAULT_CATEGORY_DESCRIPTION_TEMPLATE.format(
                    category=config["category"]
                )}
            )

            # Create quiz
            quiz = DailyQuiz.objects.create(
                date=quiz_date,
                category=category,
                title=config['title'],
                description=config.get('description', ''),
                is_released=True
            )

            # Create questions
            for i, q_data in enumerate(config['questions']):
                Question.objects.create(
                    quiz=quiz,
                    order=i + 1,
                    text=q_data['question'],
                    option_a=q_data['options'][0],
                    option_b=q_data['options'][1],
                    option_c=q_data['options'][2],
                    option_d=q_data['options'][3],
                    correct_answer=ANSWER_CHOICES[q_data['correct_answer']]
                )

            # Update upload status
            upload.status = 'imported'
            upload.error_message = ''
            upload.save()

            return True

        except Exception as e:
            upload.status = 'failed'
            upload.error_message = str(e)
            upload.save()

            self.message_user(
                request,
                f'Failed to import {upload.file.name}: {str(e)}',
                messages.ERROR
            )
            return False

    def validate_config(self, config):
        """Validate quiz configuration"""
        for field in REQUIRED_QUIZ_FIELDS:
            if field not in config:
                raise ValueError(ERROR_MISSING_FIELD.format(field=field))

        if not isinstance(config['questions'], list):
            raise ValueError(ERROR_INVALID_QUESTIONS)

        if len(config['questions']) == 0:
            raise ValueError(ERROR_NO_QUESTIONS)

        for i, question in enumerate(config['questions']):
            for field in REQUIRED_QUESTION_FIELDS:
                if field not in question:
                    raise ValueError(ERROR_MISSING_FIELD.format(field=field))

            if len(question['options']) != REQUIRED_OPTIONS_COUNT:
                raise ValueError(ERROR_INVALID_OPTIONS_COUNT.format(number=i+1))

            if (not isinstance(question['correct_answer'], int) or
                    question['correct_answer'] not in VALID_ANSWER_INDICES):
                raise ValueError(ERROR_INVALID_CORRECT_ANSWER.format(number=i+1))
