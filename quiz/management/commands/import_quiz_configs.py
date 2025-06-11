import json
import os
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from quiz.models import Category, DailyQuiz, Question


class Command(BaseCommand):
    help = 'Import quiz configurations from JSON files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Import specific file',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Import all pending quiz configs',
        )
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate files without importing',
        )

    def handle(self, *args, **options):
        config_dir = 'quiz_configs'
        pending_dir = os.path.join(config_dir, 'pending')
        imported_dir = os.path.join(config_dir, 'imported')
        
        # Ensure directories exist
        os.makedirs(pending_dir, exist_ok=True)
        os.makedirs(imported_dir, exist_ok=True)
        
        if options['file']:
            # Import specific file
            file_path = os.path.join(pending_dir, options['file'])
            if not os.path.exists(file_path):
                raise CommandError(f'File not found: {file_path}')
            
            self.process_file(file_path, imported_dir, options['validate_only'])
            
        elif options['all']:
            # Import all pending files
            json_files = [f for f in os.listdir(pending_dir) if f.endswith('.json')]
            
            if not json_files:
                self.stdout.write(self.style.WARNING('No pending quiz configs found'))
                return
            
            for filename in json_files:
                file_path = os.path.join(pending_dir, filename)
                try:
                    self.process_file(file_path, imported_dir, options['validate_only'])
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to process {filename}: {str(e)}')
                    )
        else:
            raise CommandError('Please specify --file <filename> or --all')

    def process_file(self, file_path, imported_dir, validate_only=False):
        filename = os.path.basename(file_path)
        self.stdout.write(f'Processing {filename}...')
        
        try:
            # Load and validate JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Validate configuration
            self.validate_config(config, filename)
            
            if validate_only:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {filename} is valid')
                )
                return
            
            # Import to database
            self.import_quiz(config)
            
            # Move file to imported directory
            imported_path = os.path.join(imported_dir, filename)
            shutil.move(file_path, imported_path)
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Successfully imported {filename}')
            )
            
        except json.JSONDecodeError as e:
            raise CommandError(f'Invalid JSON in {filename}: {str(e)}')
        except Exception as e:
            raise CommandError(f'Error processing {filename}: {str(e)}')

    def validate_config(self, config, filename):
        """Validate quiz configuration structure and content"""
        required_fields = ['date', 'category', 'title', 'questions']
        
        # Check required fields
        for field in required_fields:
            if field not in config:
                raise ValueError(f'Missing required field: {field}')
        
        # Validate date format
        try:
            datetime.strptime(config['date'], '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        
        # Validate questions
        questions = config['questions']
        if not isinstance(questions, list) or len(questions) == 0:
            raise ValueError('Questions must be a non-empty array')
        
        if len(questions) > 20:
            raise ValueError('Maximum 20 questions allowed per quiz')
        
        for i, question in enumerate(questions):
            self.validate_question(question, i + 1)
        
        # Check for duplicate quiz date
        if DailyQuiz.objects.filter(date=config['date']).exists():
            raise ValueError(f'Quiz for date {config["date"]} already exists')

    def validate_question(self, question, question_num):
        """Validate individual question structure"""
        required_fields = ['question', 'options', 'correct_answer']
        
        for field in required_fields:
            if field not in question:
                raise ValueError(f'Question {question_num}: Missing field {field}')
        
        # Validate options
        options = question['options']
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(f'Question {question_num}: Must have exactly 4 options')
        
        # Validate correct_answer
        correct_answer = question['correct_answer']
        if not isinstance(correct_answer, int) or correct_answer < 0 or correct_answer > 3:
            raise ValueError(f'Question {question_num}: correct_answer must be 0, 1, 2, or 3')
        
        # Check for empty strings
        if not question['question'].strip():
            raise ValueError(f'Question {question_num}: Question text cannot be empty')
        
        for i, option in enumerate(options):
            if not str(option).strip():
                raise ValueError(f'Question {question_num}: Option {i+1} cannot be empty')

    @transaction.atomic
    def import_quiz(self, config):
        """Import quiz configuration to database"""
        # Get or create category
        category, created = Category.objects.get_or_create(
            name=config['category'],
            defaults={'description': f'Questions about {config["category"]}'}
        )
        
        # Create quiz
        quiz = DailyQuiz.objects.create(
            date=config['date'],
            category=category,
            title=config['title'],
            description=config.get('description', ''),
            is_released=True
        )
        
        # Create questions
        for i, question_data in enumerate(config['questions']):
            # Map correct_answer index to letter
            answer_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
            
            Question.objects.create(
                quiz=quiz,
                order=i + 1,
                text=question_data['question'],
                option_a=question_data['options'][0],
                option_b=question_data['options'][1],
                option_c=question_data['options'][2],
                option_d=question_data['options'][3],
                correct_answer=answer_map[question_data['correct_answer']]
            )
        
        self.stdout.write(f'Created quiz: {quiz.title} with {len(config["questions"])} questions')
