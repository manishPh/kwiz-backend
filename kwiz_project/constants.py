"""
Application-wide constants for Kwiz backend.
All hardcoded values should be defined here for easy maintenance.
"""

# ============================================================================
# DOMAIN & BRANDING
# ============================================================================
DOMAIN = 'kwiz.fun'
DOMAIN_WITH_WWW = f'www.{DOMAIN}'
DOMAIN_URL = f'https://{DOMAIN}'
APP_NAME = 'Kwiz'
APP_TAGLINE = 'Daily Fresh Trivia'
APP_FULL_NAME = f'{APP_NAME} - {APP_TAGLINE}'

# ============================================================================
# DEPLOYMENT & HOSTING
# ============================================================================
RAILWAY_DOMAIN_PATTERN = '.railway.app'
NETLIFY_DOMAIN_PATTERN = '.netlify.app'

# Production domains
PRODUCTION_DOMAINS = [
    DOMAIN,
    DOMAIN_WITH_WWW,
    f'api.{DOMAIN}',  # API subdomain for Cloudflare
]

# Frontend domains (for CORS)
FRONTEND_PRODUCTION_DOMAINS = [
    f'https://{DOMAIN}',
    f'https://{DOMAIN_WITH_WWW}',
    'https://kwiz-frontend-production.railway.app',
    'https://kwiz-frontend.railway.app',
]

# Development domains
DEVELOPMENT_DOMAINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# ============================================================================
# QUIZ CONFIGURATION
# ============================================================================
# Quiz release time
DEFAULT_QUIZ_RELEASE_TIME = '00:00'  # Midnight IST

# Quiz scoring emojis
SCORE_EMOJI_EXCELLENT = '🏆'  # 90%+
SCORE_EMOJI_GREAT = '🌟'      # 80-89%
SCORE_EMOJI_GOOD = '👏'       # 70-79%
SCORE_EMOJI_OKAY = '👍'       # 60-69%
SCORE_EMOJI_TRY_AGAIN = '💪'  # <60%

# Score thresholds
SCORE_THRESHOLD_EXCELLENT = 90
SCORE_THRESHOLD_GREAT = 80
SCORE_THRESHOLD_GOOD = 70
SCORE_THRESHOLD_OKAY = 60

# ============================================================================
# SHARE TEXT TEMPLATES
# ============================================================================
SHARE_TEXT_TEMPLATE = (
    "🎬 Bollywood Kwiz #{date} 🎬\n"
    "{emoji} {score}/{total} ({percentage}%)\n\n"
    "Can you beat my score? 🤔"
)

SHARE_TEXT_SUFFIX = f"\n\nPlay daily Bollywood trivia at {DOMAIN} 🎬"

# ============================================================================
# FILE UPLOAD CONFIGURATION
# ============================================================================
QUIZ_CONFIG_UPLOAD_PATH = 'quiz_configs/uploads/'

# ============================================================================
# ADMIN CONFIGURATION
# ============================================================================
ADMIN_SITE_HEADER = f'{APP_NAME} Administration'
ADMIN_SITE_TITLE = f'{APP_NAME} Admin Portal'
ADMIN_INDEX_TITLE = 'Welcome to Kwiz Administration'

# ============================================================================
# API CONFIGURATION
# ============================================================================
API_PREFIX = '/api'
QUIZ_API_PREFIX = f'{API_PREFIX}/quiz'

# ============================================================================
# SOCIAL MEDIA
# ============================================================================
WHATSAPP_SHARE_URL = 'https://wa.me/?text='
FACEBOOK_SHARE_URL = 'https://www.facebook.com/sharer/sharer.php'
TWITTER_SHARE_URL = 'https://twitter.com/intent/tweet'
INSTAGRAM_URL = 'https://www.instagram.com/'

# ============================================================================
# ERROR MESSAGES
# ============================================================================
ERROR_NO_QUIZ_TODAY = 'No quiz available for today'
ERROR_QUIZ_ALREADY_EXISTS = 'Quiz for date {date} already exists'
ERROR_MISSING_FIELD = 'Missing required field: {field}'
ERROR_INVALID_QUESTIONS = 'Questions must be a list'
ERROR_NO_QUESTIONS = 'Quiz must have at least one question'
ERROR_INVALID_OPTIONS_COUNT = 'Question {number}: Must have exactly 4 options'
ERROR_INVALID_CORRECT_ANSWER = 'Question {number}: correct_answer must be 0, 1, 2, or 3'

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================
SUCCESS_QUIZ_IMPORTED = 'Successfully imported quiz: {title} for {date}'
SUCCESS_CONFIG_UPLOADED = 'Quiz configuration uploaded successfully'

# ============================================================================
# VALIDATION CONSTANTS
# ============================================================================
REQUIRED_QUIZ_FIELDS = ['date', 'category', 'title', 'questions']
REQUIRED_QUESTION_FIELDS = ['question', 'options', 'correct_answer']
REQUIRED_OPTIONS_COUNT = 4
VALID_ANSWER_INDICES = [0, 1, 2, 3]
ANSWER_CHOICES = ['A', 'B', 'C', 'D']

# ============================================================================
# DATE & TIME FORMATS
# ============================================================================
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M'
QUIZ_DATE_DISPLAY_FORMAT = '%d%m%Y'  # For share text
TIME_FORMAT = '%H:%M'

# ============================================================================
# CATEGORY DEFAULTS
# ============================================================================
DEFAULT_CATEGORY_DESCRIPTION_TEMPLATE = 'Questions about {category}'

