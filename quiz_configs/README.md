# 📝 Kwiz Configuration System

## Overview
This system allows non-technical team members to create quiz configurations using simple JSON files that can be easily imported into the Kwiz app.

## 🚀 Quick Start: Upload a Quiz (Recommended Method)

### For Team Members with Admin Access

1. **Create your quiz JSON file** (see format below or use `production/EXAMPLE_quiz_template.json` as template)
2. **Go to Django Admin**: `https://your-domain.com/admin/`
3. **Navigate to**: Quiz → Quiz Config Uploads
4. **Click**: "Add Quiz Config Upload"
5. **Upload your file**:
   - Click "Choose File" and select your JSON file
   - Enter your name in "Uploaded by" (optional)
   - Click "Save"
6. **Done!** The quiz is automatically imported and validated

### What Happens After Upload?

- ✅ **Success**: Status shows "Imported" in green, quiz is live
- ❌ **Error**: Status shows "Failed" in red with error message explaining the issue
- You can view all your uploads and their status in the "Quiz Config Uploads" section

### Benefits of Admin Upload

- **No command line needed** - just use the web interface
- **Automatic validation** - errors are caught and explained clearly
- **Upload history** - see all past uploads and their status
- **Team friendly** - anyone with admin access can upload quizzes
- **Works on free tier** - no shell access required

## 📋 Quiz Configuration Format

### Basic Structure
```json
{
  "date": "2025-06-09",
  "category": "Films",
  "title": "Shah Rukh Khan Birthday Special",
  "description": "Celebrating the King of Bollywood on his special day",
  "background_image": "https://example.com/srk-background.jpg",
  "questions": [
    {
      "question": "In which year was DDLJ released?",
      "options": ["1994", "1995", "1996", "1997"],
      "correct_answer": 1
    }
  ]
}
```

### Field Descriptions

#### **Quiz Metadata**
- `date` (required): Quiz date in YYYY-MM-DD format
- `category` (required): Category name (Films, Actors, Music, Sports, etc.)
- `title` (required): Quiz title (max 200 characters)
- `description` (optional): Brief description of the quiz theme
- `background_image` (optional): URL for contextual background image

#### **Questions Array**
- `question` (required): The question text
- `options` (required): Array of exactly 4 answer options
- `correct_answer` (required): Index of correct answer (0-3)

### 🎯 Example Quiz Configurations

#### Bollywood Actor Birthday
```json
{
  "date": "2025-11-02",
  "category": "Actors", 
  "title": "Shah Rukh Khan Birthday Special",
  "description": "Test your knowledge about the King of Bollywood",
  "background_image": "https://example.com/srk-collage.jpg",
  "questions": [
    {
      "question": "What was Shah Rukh Khan's debut film?",
      "options": ["Deewana", "Fauji", "Baazigar", "Darr"],
      "correct_answer": 0
    },
    {
      "question": "Which SRK film won the National Film Award?",
      "options": ["My Name is Khan", "Chak De India", "Swades", "All of the above"],
      "correct_answer": 3
    }
  ]
}
```

#### Cricket World Cup Special
```json
{
  "date": "2025-06-15",
  "category": "Sports",
  "title": "Cricket World Cup Fever",
  "description": "Cricket meets Bollywood in this special quiz",
  "background_image": "https://example.com/cricket-stadium.jpg",
  "questions": [
    {
      "question": "Which Bollywood film featured cricket as the main theme?",
      "options": ["Lagaan", "83", "M.S. Dhoni", "All of the above"],
      "correct_answer": 3
    }
  ]
}
```

## 📁 File Organization

### Directory Structure
```
kwiz-backend/
├── quiz_configs/
│   ├── README.md (this file)
│   ├── templates/
│   │   ├── bollywood_template.json
│   │   ├── sports_template.json
│   │   └── general_template.json
│   ├── pending/
│   │   ├── 2025-06-09_srk_birthday.json
│   │   ├── 2025-06-15_cricket_special.json
│   │   └── 2025-06-20_music_legends.json
│   └── imported/
│       └── (moved here after successful import)
```

### File Naming Convention
`YYYY-MM-DD_quiz_theme.json`

Examples:
- `2025-06-09_srk_birthday.json`
- `2025-06-15_cricket_worldcup.json`
- `2025-12-25_christmas_special.json`

## 🛠️ Usage Instructions for Non-Technical Team

### Step 1: Choose a Template
Copy one of the template files from the `templates/` folder based on your quiz type.

### Step 2: Fill in Your Content
1. Update the `date` field with your target quiz date
2. Set appropriate `category`, `title`, and `description`
3. Add your questions following the format
4. Ensure exactly 4 options per question
5. Set the correct answer index (0 for first option, 1 for second, etc.)

### Step 3: Validate Your Quiz
- Check that all required fields are filled
- Verify question count (recommended: 10-15 questions)
- Ensure correct_answer indices are valid (0-3)
- Test that JSON is properly formatted

### Step 4: Submit
Save your file in the `pending/` folder with the proper naming convention and notify the technical team.

## ✅ Quality Guidelines

### Content Guidelines
- **Questions**: Clear, unambiguous, and engaging
- **Options**: All options should be plausible
- **Difficulty**: Mix of easy, medium, and hard questions
- **Length**: 10-15 questions per quiz for optimal engagement

### Technical Guidelines
- **JSON Format**: Must be valid JSON (use online validators)
- **Date Format**: Always use YYYY-MM-DD
- **Answer Index**: Remember arrays start at 0 (first option = 0)
- **Character Limits**: Keep titles under 200 characters

## 🚀 Advanced Features

### Contextual Themes
Use these categories and themes for better engagement:

#### **Time-Based Themes**
- Actor/Director birthdays
- Movie release anniversaries  
- Festival celebrations
- Award ceremony dates

#### **Event-Based Themes**
- Sports tournaments (Cricket/Football World Cup)
- Music album releases
- Box office milestones
- Industry news and trends

#### **Seasonal Themes**
- Summer blockbusters
- Monsoon romance movies
- Festival season specials
- Year-end retrospectives

This system makes it super easy for anyone to create engaging, timely quizzes without touching any code! 🎬✨
