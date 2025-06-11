# 🚀 Quiz Creation Workflow

## For Non-Technical Team Members

### Step 1: Choose Your Template 📋
Copy one of these templates based on your quiz type:
- `templates/bollywood_template.json` - For films, actors, music
- `templates/sports_template.json` - For sports-related quizzes

### Step 2: Create Your Quiz 📝
1. **Copy template** to `pending/` folder
2. **Rename file** using format: `YYYY-MM-DD_theme_name.json`
   - Example: `2025-06-15_cricket_worldcup.json`
3. **Fill in your content**:
   - Update `date` (when quiz should go live)
   - Set `category`, `title`, `description`
   - Replace template questions with your content
   - Set correct answers (remember: 0=first option, 1=second, etc.)

### Step 3: Validate Your Quiz ✅
Run the validator to check for errors:
```bash
python validate_quiz.py your_filename.json
```

Or validate all pending quizzes:
```bash
python validate_quiz.py --all
```

### Step 4: Submit for Import 📤
Once validation passes:
1. **Notify technical team** that quiz is ready
2. **Provide the filename** and target date
3. Technical team will import using: `python manage.py import_quiz_configs --file your_filename.json`

---

## For Technical Team Members

### Import Single Quiz
```bash
cd kwiz-backend
python manage.py import_quiz_configs --file 2025-06-10_srk_birthday.json
```

### Import All Pending Quizzes
```bash
python manage.py import_quiz_configs --all
```

### Validate Before Import
```bash
python manage.py import_quiz_configs --validate-only --all
```

### File Organization
- `pending/` - New quiz configs waiting to be imported
- `imported/` - Successfully imported configs (moved automatically)
- `templates/` - Template files for creating new quizzes

---

## Quick Reference

### Quiz Configuration Format
```json
{
  "date": "2025-06-15",
  "category": "Films",
  "title": "Quiz Title",
  "description": "Brief description",
  "background_image": "https://example.com/image.jpg",
  "questions": [
    {
      "question": "Your question?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": 0
    }
  ]
}
```

### Answer Index Reference
- `0` = First option (A)
- `1` = Second option (B)  
- `2` = Third option (C)
- `3` = Fourth option (D)

### Recommended Categories
- `Films` - Movies, cinema
- `Actors` - Male actors
- `Actresses` - Female actors  
- `Music` - Songs, composers
- `Sports` - Cricket, football, etc.
- `General` - Mixed topics

### Content Guidelines
- **10-15 questions** per quiz (optimal engagement)
- **Mix difficulty levels** (easy, medium, hard)
- **Clear, unambiguous questions**
- **All options should be plausible**
- **Avoid very long text** in questions/options

---

## Example Themes

### 🎬 Bollywood Themes
- Actor/actress birthdays
- Movie anniversaries
- Award ceremony dates
- Festival celebrations
- Director spotlights

### 🏏 Sports Themes  
- World Cup events
- Olympic games
- IPL seasons
- Sports movie releases
- Athlete achievements

### 📅 Seasonal Themes
- New Year specials
- Valentine's Day romance
- Independence Day patriotic
- Diwali celebrations
- Summer blockbusters

This system makes quiz creation super simple while maintaining quality and consistency! 🎯✨
