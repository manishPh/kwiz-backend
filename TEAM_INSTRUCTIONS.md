# Team Instructions: How to Upload Quizzes

## 🎯 Quick Guide for Non-Technical Team Members

You can now upload quizzes directly through the web interface - no coding or command line needed!

### Step-by-Step Process

#### 1. Create Your Quiz JSON File

- Use the template: `quiz_configs/production/EXAMPLE_quiz_template.json`
- Copy it and rename to: `YYYY-MM-DD_quiz_name.json`
  - Example: `2025-01-15_bollywood_classics.json`
- Edit the file with your quiz content

#### 2. Access Django Admin

- Go to: `https://your-railway-domain.railway.app/admin/`
- Log in with your superuser credentials

#### 3. Upload Your Quiz

1. Click on **"Quiz"** section in the left sidebar
2. Click on **"Quiz Config Uploads"**
3. Click the **"Add Quiz Config Upload"** button (top right)
4. Fill in the form:
   - **File**: Click "Choose File" and select your JSON file
   - **Uploaded by**: Type your name (optional but recommended)
5. Click **"Save"** button

#### 4. Verify Success

After clicking Save, you'll be redirected to the upload details page:

**✅ Success:**
- Status shows **"Imported"** in green
- Quiz date and title are displayed
- No error message

**❌ Failed:**
- Status shows **"Failed"** in red
- Error message explains what went wrong
- Fix the issue in your JSON file and upload again

#### 5. Check Your Quiz

1. Go back to the main admin page
2. Click **"Daily Quizzes"**
3. Find your quiz by date
4. Click on it to see all questions
5. Verify everything looks correct

---

## 📝 JSON File Format

### Required Structure

```json
{
  "date": "2025-01-15",
  "category": "Movies",
  "title": "Your Quiz Title",
  "description": "Brief description of the quiz",
  "questions": [
    {
      "question": "Your question text?",
      "options": [
        "Option A",
        "Option B", 
        "Option C",
        "Option D"
      ],
      "correct_answer": 0
    }
  ]
}
```

### Important Rules

- **Date**: Must be `YYYY-MM-DD` format and unique (no duplicates)
- **Category**: Common ones: Movies, Actors, Music, Sports, History
- **Questions**: Include 5-15 questions
- **Options**: Must have exactly 4 options
- **Correct Answer**: Use numbers: 0=A, 1=B, 2=C, 3=D

---

## 🔍 Common Errors

### "Quiz for date YYYY-MM-DD already exists"
**Fix**: Change the date to one that doesn't have a quiz yet

### "Missing required field: X"
**Fix**: Add the missing field (date, category, title, or questions)

### "Question X: Must have exactly 4 options"
**Fix**: Make sure each question has exactly 4 options in the array

### "Question X: correct_answer must be 0, 1, 2, or 3"
**Fix**: Use a number (0, 1, 2, or 3), not a letter

### "Invalid JSON"
**Fix**: 
- Check for missing commas
- Remove trailing commas (last item shouldn't have comma)
- Validate at: https://jsonlint.com/

---

## 💡 Tips for Great Quizzes

1. **Pick a Theme**: Birthday, anniversary, trending topic, festival
2. **Mix Difficulty**: Easy, medium, and hard questions
3. **Verify Facts**: Double-check all answers are correct
4. **Clear Questions**: No ambiguity
5. **Good Options**: Make all options plausible
6. **Proofread**: Check spelling and grammar

---

## 📚 Examples

See these files for reference:
- `quiz_configs/production/EXAMPLE_quiz_template.json` - Basic template
- `quiz_configs/production/2024-12-29_rajesh_khanna_birthday.json` - Complete example

---

## 🆘 Need Help?

1. Check the error message in the admin panel
2. Validate your JSON at https://jsonlint.com/
3. Compare with the example files
4. Contact the tech team

---

## 🚀 For Today: Import Rajesh Khanna Quiz

To import the Rajesh Khanna quiz that's ready:

1. Go to admin: `https://your-domain.railway.app/admin/`
2. Navigate to: Quiz → Quiz Config Uploads
3. Click: "Add Quiz Config Upload"
4. Upload: `quiz_configs/production/2024-12-29_rajesh_khanna_birthday.json`
5. Uploaded by: Your name
6. Click: Save

The quiz will be live immediately!

