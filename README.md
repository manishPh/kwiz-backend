# Kwiz Backend API

Django REST API for the Kwiz Bollywood trivia app.

## Features
- Quiz management with JSON configuration
- Daily quiz system with timer functionality
- User statistics and analytics
- CORS enabled for frontend integration
- PostgreSQL database support

## Quick Start

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Production (Railway)
1. Generate secret key: `python generate_secret_key.py`
2. Set environment variables in Railway:
   - `SECRET_KEY`: Generated secret key
   - `DEBUG`: False
3. Deploy to Railway - auto-detects Django

## API Endpoints
- `GET /api/quiz/current/` - Get current daily quiz
- `GET /api/quiz/stats/` - Get user statistics
- `POST /api/quiz/submit/` - Submit quiz answers

## Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: PostgreSQL connection (auto-set by Railway)

## Tech Stack
- Django 4.2
- Django REST Framework
- PostgreSQL (production) / SQLite (development)
- Gunicorn (WSGI server)
kwiz-backend
