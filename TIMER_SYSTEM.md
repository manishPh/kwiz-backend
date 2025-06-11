# ⏰ Kwiz Timer & Release System

## Overview
Kwiz.com implements a **Wordle-inspired daily release system** where new quizzes are released at a fixed time each day, creating anticipation and community engagement.

## 🕐 How It Works (Like Wordle)

### **Global Synchronized Release**
- **Fixed Daily Schedule**: New quiz releases at **12:00 AM IST** every day
- **Same Quiz for Everyone**: All users worldwide get the same quiz on the same day
- **No User Tracking**: Not based on individual cookies or play history
- **Community Building**: Everyone discusses the same quiz on social media

### **Timer Countdown**
- **Real-time Countdown**: Shows hours:minutes:seconds until next release
- **Auto-refresh**: Page refreshes when quiz becomes available
- **Visual Feedback**: Beautiful countdown with contextual messages

## 🛠️ Technical Implementation

### **Backend (Django)**

#### **Models Enhancement**
```python
class DailyQuiz(models.Model):
    date = models.DateField(unique=True)
    release_time = models.TimeField(default="00:00")  # IST timezone
    is_released = models.BooleanField(default=True)
    
    def is_quiz_released(self):
        """Check if quiz should be released based on IST timezone"""
        # Uses pytz for accurate timezone handling
        
    def get_time_until_release(self):
        """Get seconds remaining until quiz release"""
        
    def get_next_quiz_info(self):
        """Get information about upcoming quiz"""
```

#### **New API Endpoints**
- `GET /api/quiz/status/` - Get today's quiz status and timer
- `GET /api/quiz/status/<date>/` - Get specific date quiz status
- Enhanced `GET /api/quiz/daily/<date>/` - Returns timer info when not available

#### **API Response Format**
```json
{
  "quiz_date": "2025-06-09",
  "quiz_title": "Shah Rukh Khan Birthday Special",
  "category": "Actors",
  "is_available": false,
  "time_until_release": 3600,
  "next_quiz": {
    "date": "2025-06-10",
    "title": "Cricket World Cup Special",
    "category": "Sports",
    "time_until_release": 86400
  },
  "release_time": "00:00"
}
```

### **Frontend (React)**

#### **QuizTimer Component**
- **Real-time Countdown**: Updates every second
- **Auto-refresh**: Reloads page when quiz becomes available
- **Responsive Design**: Mobile-optimized display
- **Visual Appeal**: Gradient backgrounds, animations

#### **Integration**
```javascript
// HomePage checks quiz status first
const status = await quizAPI.getQuizStatus(today);

if (status.is_available) {
  // Load and show quiz
} else {
  // Show countdown timer
}
```

## 🎯 User Experience

### **When Quiz is Available**
- Normal quiz interface
- "Start Today's Kwiz" button
- Background image based on theme

### **When Quiz is Not Available**
- Beautiful countdown timer
- Quiz title and category preview
- "Coming Soon" messaging
- Release time information (12:00 AM IST)

### **Timer Display**
```
Next Quiz Coming Soon
Shah Rukh Khan Birthday Special

02:45:30
Coming today!

⏰ Releases at 12:00 AM IST  🎬 Actors
```

## 📅 Content Strategy Integration

### **Scheduled Releases**
- **Actor Birthdays**: Quiz releases on their birthday at midnight
- **Movie Anniversaries**: Quiz about the movie on anniversary date
- **Sports Events**: Quiz during tournament/match days
- **Festivals**: Special themed quizzes on festival dates

### **Example Schedule**
```
2025-06-09: Shah Rukh Khan Birthday Special (Actors)
2025-06-10: Cricket World Cup Fever (Sports)  
2025-06-11: DDLJ 30th Anniversary (Films)
2025-06-12: Music Legends Friday (Music)
```

## 🔧 Setup & Management

### **Install Dependencies**
```bash
pip install pytz==2023.3
```

### **Database Migration**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **Set Quiz Release Times**
```bash
# Set all quizzes to release at midnight IST
python manage.py setup_quiz_schedule --days 7 --release-time 00:00

# Set custom release time (e.g., 6 AM IST)
python manage.py setup_quiz_schedule --days 30 --release-time 06:00
```

### **Create Future Quizzes**
1. Use quiz creator or JSON templates
2. Set future dates in quiz configs
3. Import using management command
4. Quiz will automatically become available at release time

## 🌍 Timezone Handling

### **IST (Indian Standard Time)**
- **Primary Timezone**: All releases based on IST
- **Global Access**: Users worldwide see countdown to IST midnight
- **Consistent Experience**: Same quiz available to everyone simultaneously

### **Why IST?**
- **Target Audience**: Primary users in India
- **Bollywood Context**: Aligns with Indian entertainment industry
- **Simple Implementation**: Single timezone reduces complexity

## 🚀 Benefits

### **User Engagement**
- **Daily Habit**: Users return at specific time each day
- **FOMO Effect**: "Today only" creates urgency
- **Social Sharing**: Everyone discusses same quiz simultaneously
- **Anticipation**: Countdown builds excitement

### **Content Strategy**
- **Event-Driven**: Quizzes tied to real-world events
- **Timely Relevance**: Content matches current happenings
- **Viral Potential**: Shared experience drives social media engagement

### **Technical Benefits**
- **Server Load**: Predictable traffic patterns
- **Caching**: Easy to cache quiz data
- **Analytics**: Clear daily engagement metrics

## 📱 Mobile Experience

### **Optimized Timer**
- **Large Countdown**: Easy to read on mobile
- **Touch-Friendly**: Proper spacing and sizing
- **Battery Efficient**: Minimal JavaScript processing
- **Offline Handling**: Graceful degradation

### **Push Notifications (Future)**
- **Daily Reminders**: "New quiz available!"
- **Custom Times**: User can set preferred notification time
- **Streak Alerts**: "Don't break your 7-day streak!"

## 🔮 Future Enhancements

### **Advanced Scheduling**
- **Multiple Timezones**: Regional release times
- **Custom Schedules**: Different release times for different categories
- **Holiday Adjustments**: Special timing for festivals

### **Enhanced Timer**
- **Animated Countdown**: More engaging visuals
- **Sound Alerts**: Optional audio notifications
- **Preview Content**: Sneak peek of upcoming quiz

### **Analytics**
- **Timer Engagement**: How long users wait
- **Peak Times**: When most users check for new quizzes
- **Conversion Rates**: Timer views to quiz completions

This timer system transforms Kwiz.com from a simple quiz app into an anticipated daily event that users look forward to! ⏰🎬✨
