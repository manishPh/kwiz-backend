from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date
import pytz
from .models import DailyQuiz, Question
from .serializers import (
    QuizSerializer,
    QuizResultSerializer,
    QuestionResultSerializer,
    ArchiveQuizSerializer
)
from kwiz_project.constants import (
    SCORE_EMOJI_EXCELLENT, SCORE_EMOJI_GREAT, SCORE_EMOJI_GOOD,
    SCORE_EMOJI_OKAY, SCORE_EMOJI_TRY_AGAIN,
    SCORE_THRESHOLD_EXCELLENT, SCORE_THRESHOLD_GREAT,
    SCORE_THRESHOLD_GOOD, SCORE_THRESHOLD_OKAY,
    QUIZ_DATE_DISPLAY_FORMAT, ERROR_NO_QUIZ_TODAY
)


@api_view(['GET'])
def get_daily_quiz(request, quiz_date):
    """Get daily quiz for a specific date"""
    try:
        quiz = get_object_or_404(DailyQuiz, date=quiz_date)

        # Check if quiz is available
        if not quiz.is_available:
            time_until_release = quiz.get_time_until_release()
            next_quiz_info = quiz.get_next_quiz_info()

            return Response({
                'error': 'Quiz not yet available',
                'quiz_date': quiz.date,
                'quiz_title': quiz.title,
                'time_until_release': time_until_release,
                'next_quiz': next_quiz_info,
                'message': f'This quiz will be available soon!'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = QuizSerializer(quiz)
        quiz_data = serializer.data

        # Add timer information for frontend
        quiz_data['time_until_release'] = 0  # Already available
        quiz_data['next_quiz'] = quiz.get_next_quiz_info()

        return Response(quiz_data)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def submit_quiz(request):
    """Submit quiz answers and get results"""
    serializer = QuizResultSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    quiz_date = serializer.validated_data['date']
    answers = serializer.validated_data['answers']

    try:
        quiz = get_object_or_404(DailyQuiz, date=quiz_date)
        questions = quiz.questions.all()

        # Calculate score
        score = 0
        total_questions = len(questions)
        results = []

        # Create answer mapping
        answer_map = {}
        for answer in answers:
            answer_map[int(answer['question_id'])] = answer['selected_option']

        for question in questions:
            user_answer = answer_map.get(question.id, '')
            correct_option_map = {
                'A': question.option_a,
                'B': question.option_b,
                'C': question.option_c,
                'D': question.option_d,
            }
            correct_answer_text = correct_option_map[question.correct_answer]
            is_correct = user_answer == correct_answer_text

            if is_correct:
                score += 1

            results.append({
                'question_id': question.id,
                'correct': is_correct,
                'correct_answer': correct_answer_text,
                'user_answer': user_answer
            })

        percentage = round((score / total_questions) * 100) if total_questions > 0 else 0

        # Generate share text with emojis and engagement
        if percentage >= SCORE_THRESHOLD_EXCELLENT:
            emoji_score = SCORE_EMOJI_EXCELLENT
        elif percentage >= SCORE_THRESHOLD_GREAT:
            emoji_score = SCORE_EMOJI_GREAT
        elif percentage >= SCORE_THRESHOLD_GOOD:
            emoji_score = SCORE_EMOJI_GOOD
        elif percentage >= SCORE_THRESHOLD_OKAY:
            emoji_score = SCORE_EMOJI_OKAY
        else:
            emoji_score = SCORE_EMOJI_TRY_AGAIN

        share_text = (f"🎬 Bollywood Kwiz #{quiz_date.strftime(QUIZ_DATE_DISPLAY_FORMAT)} 🎬\n"
                     f"{emoji_score} {score}/{total_questions} ({percentage}%)\n\n"
                     f"Can you beat my score? 🤔")

        return Response({
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'results': results,
            'share_text': share_text
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_quiz_archive(request):
    """Get list of available past quizzes"""
    try:
        quizzes = DailyQuiz.objects.filter(
            date__lte=date.today(),
            is_released=True
        ).order_by('-date')[:30]  # Last 30 quizzes

        serializer = ArchiveQuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_quiz_status(request, quiz_date=None):
    """Get quiz availability status and timer information"""
    try:
        if quiz_date:
            quiz = get_object_or_404(DailyQuiz, date=quiz_date)
        else:
            # Get today's quiz
            today = date.today()
            quiz = DailyQuiz.objects.filter(date=today).first()

            if not quiz:
                next_quiz = DailyQuiz.objects.filter(date__gt=today).first()
                next_quiz_info = None
                if next_quiz:
                    next_quiz_info = {
                        'date': next_quiz.date,
                        'title': next_quiz.title,
                        'category': next_quiz.category.name,
                        'time_until_release': next_quiz.get_time_until_release()
                    }

                return Response({
                    'error': ERROR_NO_QUIZ_TODAY,
                    'next_quiz': next_quiz_info
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'quiz_date': quiz.date,
            'quiz_title': quiz.title,
            'category': quiz.category.name,
            'is_available': quiz.is_available,
            'time_until_release': quiz.get_time_until_release(),
            'next_quiz': quiz.get_next_quiz_info(),
            'release_time': quiz.release_time.strftime('%H:%M') if quiz.release_time else '00:00'
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
