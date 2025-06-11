#!/usr/bin/env python3
"""
Quiz Configuration Validator
============================

This script helps non-technical team members validate their quiz JSON files
before submitting them for import.

Usage:
    python validate_quiz.py filename.json
    python validate_quiz.py --all  # validate all files in pending/

Requirements:
    - Python 3.6+
    - No additional dependencies needed
"""

import json
import os
import sys
from datetime import datetime


def validate_quiz_config(config, filename):
    """Validate quiz configuration and return list of errors"""
    errors = []
    warnings = []
    
    # Check required fields
    required_fields = ['date', 'category', 'title', 'questions']
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: '{field}'")
    
    if errors:
        return errors, warnings  # Return early if missing required fields
    
    # Validate date
    try:
        quiz_date = datetime.strptime(config['date'], '%Y-%m-%d')
        if quiz_date < datetime.now():
            warnings.append(f"Quiz date {config['date']} is in the past")
    except ValueError:
        errors.append("Date must be in YYYY-MM-DD format (e.g., '2025-06-09')")
    
    # Validate title
    if len(config['title']) > 200:
        errors.append("Title must be 200 characters or less")
    if not config['title'].strip():
        errors.append("Title cannot be empty")
    
    # Validate category
    valid_categories = ['Films', 'Actors', 'Actresses', 'Music', 'Sports', 'General']
    if config['category'] not in valid_categories:
        warnings.append(f"Category '{config['category']}' is not in recommended list: {valid_categories}")
    
    # Validate questions
    questions = config['questions']
    if not isinstance(questions, list):
        errors.append("Questions must be an array")
        return errors, warnings
    
    if len(questions) == 0:
        errors.append("Must have at least 1 question")
    elif len(questions) < 5:
        warnings.append(f"Only {len(questions)} questions. Recommended: 10-15 questions")
    elif len(questions) > 20:
        errors.append(f"Too many questions ({len(questions)}). Maximum: 20 questions")
    elif len(questions) > 15:
        warnings.append(f"{len(questions)} questions might be too long. Recommended: 10-15")
    
    # Validate each question
    for i, question in enumerate(questions):
        q_errors, q_warnings = validate_question(question, i + 1)
        errors.extend(q_errors)
        warnings.extend(q_warnings)
    
    return errors, warnings


def validate_question(question, question_num):
    """Validate individual question"""
    errors = []
    warnings = []
    
    # Check required fields
    required_fields = ['question', 'options', 'correct_answer']
    for field in required_fields:
        if field not in question:
            errors.append(f"Question {question_num}: Missing '{field}' field")
    
    if errors:
        return errors, warnings
    
    # Validate question text
    if not question['question'].strip():
        errors.append(f"Question {question_num}: Question text cannot be empty")
    elif len(question['question']) > 500:
        warnings.append(f"Question {question_num}: Question text is very long ({len(question['question'])} chars)")
    
    # Validate options
    options = question['options']
    if not isinstance(options, list):
        errors.append(f"Question {question_num}: Options must be an array")
    elif len(options) != 4:
        errors.append(f"Question {question_num}: Must have exactly 4 options (found {len(options)})")
    else:
        for i, option in enumerate(options):
            if not str(option).strip():
                errors.append(f"Question {question_num}: Option {i+1} cannot be empty")
            elif len(str(option)) > 200:
                warnings.append(f"Question {question_num}: Option {i+1} is very long")
    
    # Validate correct_answer
    correct_answer = question['correct_answer']
    if not isinstance(correct_answer, int):
        errors.append(f"Question {question_num}: correct_answer must be a number (0, 1, 2, or 3)")
    elif correct_answer < 0 or correct_answer > 3:
        errors.append(f"Question {question_num}: correct_answer must be 0, 1, 2, or 3 (found {correct_answer})")
    
    return errors, warnings


def validate_file(filepath):
    """Validate a single quiz file"""
    filename = os.path.basename(filepath)
    print(f"\n📝 Validating {filename}...")
    print("=" * 50)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    errors, warnings = validate_quiz_config(config, filename)
    
    # Display results
    if errors:
        print("❌ ERRORS (must fix before import):")
        for error in errors:
            print(f"   • {error}")
    
    if warnings:
        print("⚠️  WARNINGS (recommended to fix):")
        for warning in warnings:
            print(f"   • {warning}")
    
    if not errors and not warnings:
        print("✅ Perfect! No issues found.")
    elif not errors:
        print("✅ Valid! Only minor warnings above.")
    else:
        print("❌ Invalid! Please fix errors above.")
    
    # Show quiz summary
    if not errors:
        print(f"\n📊 Quiz Summary:")
        print(f"   Date: {config['date']}")
        print(f"   Category: {config['category']}")
        print(f"   Title: {config['title']}")
        print(f"   Questions: {len(config['questions'])}")
        if 'description' in config:
            print(f"   Description: {config['description'][:50]}...")
    
    return len(errors) == 0


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python validate_quiz.py filename.json")
        print("  python validate_quiz.py --all")
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        # Validate all files in pending directory
        pending_dir = 'pending'
        if not os.path.exists(pending_dir):
            print(f"❌ Directory '{pending_dir}' not found")
            sys.exit(1)
        
        json_files = [f for f in os.listdir(pending_dir) if f.endswith('.json')]
        if not json_files:
            print("No JSON files found in pending/ directory")
            sys.exit(0)
        
        print(f"🔍 Found {len(json_files)} quiz files to validate")
        
        valid_count = 0
        for filename in json_files:
            filepath = os.path.join(pending_dir, filename)
            if validate_file(filepath):
                valid_count += 1
        
        print(f"\n📈 Summary: {valid_count}/{len(json_files)} files are valid")
        
    else:
        # Validate single file
        filename = sys.argv[1]
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Check in current directory first, then pending/
        if os.path.exists(filename):
            filepath = filename
        elif os.path.exists(os.path.join('pending', filename)):
            filepath = os.path.join('pending', filename)
        else:
            print(f"❌ File not found: {filename}")
            print("Make sure the file is in the current directory or pending/ folder")
            sys.exit(1)
        
        is_valid = validate_file(filepath)
        sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
