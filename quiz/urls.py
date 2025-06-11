from django.urls import path
from . import views

urlpatterns = [
    path('daily/<str:quiz_date>/', views.get_daily_quiz, name='daily_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('archive/', views.get_quiz_archive, name='quiz_archive'),
    path('status/', views.get_quiz_status, name='quiz_status'),
    path('status/<str:quiz_date>/', views.get_quiz_status, name='quiz_status_date'),
]
