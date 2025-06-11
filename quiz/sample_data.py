"""
Sample Bollywood quiz data for testing
"""

from datetime import date, timedelta
from .models import Category, DailyQuiz, Question


def create_sample_data():
    """Create sample Bollywood quiz data"""
    
    # Create categories
    films_category, _ = Category.objects.get_or_create(
        name="Films",
        defaults={"description": "Questions about Bollywood movies"}
    )
    
    actors_category, _ = Category.objects.get_or_create(
        name="Actors",
        defaults={"description": "Questions about Bollywood actors"}
    )
    
    # Create today's quiz
    today = date.today()
    quiz, created = DailyQuiz.objects.get_or_create(
        date=today,
        defaults={
            "category": films_category,
            "title": "Shah Rukh Khan Birthday Special",
            "description": "Celebrating the King of Bollywood",
            "is_released": True
        }
    )
    
    if created:
        # Sample questions for today's quiz
        questions_data = [
            {
                "order": 1,
                "text": "In which year was the movie 'Dilwale Dulhania Le Jayenge' released?",
                "option_a": "1994",
                "option_b": "1995",
                "option_c": "1996",
                "option_d": "1997",
                "correct_answer": "B"
            },
            {
                "order": 2,
                "text": "Who directed the movie 'Zindagi Na Milegi Dobara'?",
                "option_a": "Zoya Akhtar",
                "option_b": "Farhan Akhtar",
                "option_c": "Karan Johar",
                "option_d": "Yash Chopra",
                "correct_answer": "A"
            },
            {
                "order": 3,
                "text": "Which movie won the National Film Award for Best Feature Film in 2023?",
                "option_a": "RRR",
                "option_b": "Gangubai Kathiawadi",
                "option_c": "The Kashmir Files",
                "option_d": "Brahmastra",
                "correct_answer": "A"
            },
            {
                "order": 4,
                "text": "In 'Sholay', what was the name of Dharmendra's character?",
                "option_a": "Jai",
                "option_b": "Veeru",
                "option_c": "Thakur",
                "option_d": "Gabbar",
                "correct_answer": "B"
            },
            {
                "order": 5,
                "text": "Which actress played the lead role in 'Queen'?",
                "option_a": "Deepika Padukone",
                "option_b": "Priyanka Chopra",
                "option_c": "Kangana Ranaut",
                "option_d": "Alia Bhatt",
                "correct_answer": "C"
            },
            {
                "order": 6,
                "text": "Who composed the music for 'Lagaan'?",
                "option_a": "A.R. Rahman",
                "option_b": "Ilaiyaraaja",
                "option_c": "Shankar-Ehsaan-Loy",
                "option_d": "Vishal-Shekhar",
                "correct_answer": "A"
            },
            {
                "order": 7,
                "text": "In which movie did Amitabh Bachchan play a character named Vijay Deenanath Chauhan?",
                "option_a": "Sholay",
                "option_b": "Agneepath",
                "option_c": "Zanjeer",
                "option_d": "Deewaar",
                "correct_answer": "B"
            },
            {
                "order": 8,
                "text": "Which movie marked Hrithik Roshan's debut as an actor?",
                "option_a": "Kaho Naa... Pyaar Hai",
                "option_b": "Mission Kashmir",
                "option_c": "Fiza",
                "option_d": "Koi... Mil Gaya",
                "correct_answer": "A"
            },
            {
                "order": 9,
                "text": "Who directed the movie '3 Idiots'?",
                "option_a": "Aamir Khan",
                "option_b": "Rajkumar Hirani",
                "option_c": "Vidhu Vinod Chopra",
                "option_d": "Imtiaz Ali",
                "correct_answer": "B"
            },
            {
                "order": 10,
                "text": "In 'Mughal-E-Azam', who played the role of Anarkali?",
                "option_a": "Madhubala",
                "option_b": "Meena Kumari",
                "option_c": "Nargis",
                "option_d": "Waheeda Rehman",
                "correct_answer": "A"
            }
        ]
        
        for q_data in questions_data:
            Question.objects.create(quiz=quiz, **q_data)
    
    # Create yesterday's quiz for archive
    yesterday = today - timedelta(days=1)
    yesterday_quiz, created = DailyQuiz.objects.get_or_create(
        date=yesterday,
        defaults={
            "category": actors_category,
            "title": "Bollywood Legends",
            "description": "Test your knowledge about legendary actors",
            "is_released": True
        }
    )
    
    print(f"Sample data created successfully!")
    print(f"Today's quiz: {quiz}")
    print(f"Yesterday's quiz: {yesterday_quiz}")


if __name__ == "__main__":
    create_sample_data()
