from django.contrib import admin
from .models import Category, DailyQuiz, Question


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
