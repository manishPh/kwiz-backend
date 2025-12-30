#!/usr/bin/env python
"""
Import Rajesh Khanna Birthday Quiz for Dec 29, 2024
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kwiz_project.settings')
django.setup()

from quiz.models import Category, DailyQuiz, Question
from datetime import date

# Check if quiz already exists
quiz_date = date(2024, 12, 29)
if DailyQuiz.objects.filter(date=quiz_date).exists():
    print(f"Quiz for {quiz_date} already exists. Deleting and recreating...")
    DailyQuiz.objects.filter(date=quiz_date).delete()

# Get or create category
category, _ = Category.objects.get_or_create(
    name='Actors',
    defaults={'description': 'Questions about Bollywood actors'}
)

# Create quiz
quiz = DailyQuiz.objects.create(
    date=quiz_date,
    category=category,
    title='Rajesh Khanna Birthday Special',
    description="Celebrating India's first superstar on his birthday - test your knowledge about the legendary Rajesh Khanna",
    is_released=True
)

# Quiz questions
questions_data = [
    {
        "text": "What was Rajesh Khanna's real birth name?",
        "options": ["Jatin Khanna", "Rajesh Kumar", "Kaka Khanna", "Ravi Khanna"],
        "correct": 0
    },
    {
        "text": "On which date was Rajesh Khanna born?",
        "options": ["December 25, 1942", "December 29, 1942", "January 1, 1943", "November 2, 1942"],
        "correct": 1
    },
    {
        "text": "Which 1969 film made Rajesh Khanna an overnight sensation and superstar?",
        "options": ["Do Raaste", "Bandhan", "Aradhana", "Kati Patang"],
        "correct": 2
    },
    {
        "text": "What was Rajesh Khanna's debut film in 1966?",
        "options": ["Raaz", "Aakhri Khat", "Baharon Ke Sapne", "Aurat"],
        "correct": 1
    },
    {
        "text": "Which actress did Rajesh Khanna marry in 1973?",
        "options": ["Sharmila Tagore", "Mumtaz", "Dimple Kapadia", "Asha Parekh"],
        "correct": 2
    },
    {
        "text": "For which film did Rajesh Khanna win his first Filmfare Award for Best Actor?",
        "options": ["Anand", "Sachaa Jhutha", "Aradhana", "Bawarchi"],
        "correct": 1
    },
    {
        "text": "In which film did Rajesh Khanna play a cancer patient, considered his career-best performance?",
        "options": ["Safar", "Anand", "Amar Prem", "Namak Haraam"],
        "correct": 1
    },
    {
        "text": "How many consecutive hit films did Rajesh Khanna deliver between 1969-1971?",
        "options": ["12 films", "15 films", "17 films", "20 films"],
        "correct": 2
    },
    {
        "text": "Which 1973 Yash Chopra film starring Rajesh Khanna laid the foundation of Yash Raj Films?",
        "options": ["Namak Haraam", "Daag: A Poem of Love", "Raja Rani", "Prem Nagar"],
        "correct": 1
    },
    {
        "text": "Who is Rajesh Khanna's famous son-in-law (married to daughter Twinkle)?",
        "options": ["Akshay Kumar", "Aamir Khan", "Saif Ali Khan", "Ajay Devgn"],
        "correct": 0
    },
    {
        "text": "Which playback singer became the leading voice of Hindi cinema largely due to Rajesh Khanna's films?",
        "options": ["Mohammed Rafi", "Mukesh", "Kishore Kumar", "Manna Dey"],
        "correct": 2
    },
    {
        "text": "In which year did Rajesh Khanna serve as a Member of Parliament from New Delhi?",
        "options": ["1984-1989", "1989-1991", "1992-1996", "1996-2001"],
        "correct": 2
    },
    {
        "text": "Which 1972 Hrishikesh Mukherjee film starring Rajesh Khanna is considered a cult classic today?",
        "options": ["Anand", "Bawarchi", "Namak Haraam", "Avishkaar"],
        "correct": 1
    },
    {
        "text": "What prestigious award was Rajesh Khanna posthumously awarded in 2013?",
        "options": ["Bharat Ratna", "Padma Vibhushan", "Padma Bhushan", "Padma Shri"],
        "correct": 2
    },
    {
        "text": "On which date did Rajesh Khanna pass away?",
        "options": ["July 18, 2012", "July 20, 2012", "June 18, 2012", "August 18, 2012"],
        "correct": 0
    }
]

# Create questions
answer_map = ['A', 'B', 'C', 'D']
for i, q_data in enumerate(questions_data):
    Question.objects.create(
        quiz=quiz,
        order=i + 1,
        text=q_data['text'],
        option_a=q_data['options'][0],
        option_b=q_data['options'][1],
        option_c=q_data['options'][2],
        option_d=q_data['options'][3],
        correct_answer=answer_map[q_data['correct']]
    )

print(f"✓ Successfully created quiz: {quiz.title}")
print(f"  Date: {quiz.date}")
print(f"  Category: {quiz.category.name}")
print(f"  Questions: {quiz.questions.count()}")
print(f"  Is Released: {quiz.is_released}")
print(f"  Is Available: {quiz.is_available}")

