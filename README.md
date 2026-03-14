# 🎓 Personalized Tutor Agent

An AI-powered Intelligent Tutoring System with Groq AI integration for personalized learning experiences. The app adapts to student knowledge levels through dynamic assessments and generates customized learning paths.

## ⚡ Quick Start

### Installation
For detailed step-by-step installation guide, see [INSTALLATION.md](INSTALLATION.md)

**Quick version:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add API key to settings.json
# Get free key from https://console.groq.com

# 3. Run application
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🌟 Key Features

- **AI-Powered Questions** - Groq AI generates custom questions dynamically for any topic
- **5-Question Assessment** - Comprehensive diagnostic test with progressive difficulty (Easy → Hard)
- **Inline Feedback System** - Real-time feedback appears immediately after answering, showing:
  - ✅/❌ Correctness indicator
  - Correct answer revealed
  - Detailed AI-generated explanation
- **Adaptive Difficulty Progression** - Questions increase in difficulty: Easy → Easy-Medium → Medium → Medium-Hard → Hard
- **Student Level Detection** - Automatically determines proficiency:
  - **Beginner** (0-2/5 correct)
  - **Intermediate** (3/5 correct)
  - **Advanced** (4-5/5 correct)
- **Personalized Learning Paths** - AI generates course-specific learning sequences based on assessment results
- **Structured Learning Flow** - Multi-step learning with:
  - 📖 Concept Explanations
  - 💡 Real-world Examples
  - 🎯 Interactive Quizzes
  - ✅ Progress Tracking
- **Knowledge Tracing** - Tracks student mastery using simplified DKT model
- **Performance Analytics** - Monitor progress through dashboards and detailed breakdowns

## 📊 User Flow

1. **🔐 Authentication** - Sign in or register with email
2. **🎯 Subject Selection** - Choose learning subject (Mathematics, Physics, Chemistry)
3. **📚 Course Selection** - Select specific course within subject
4. **📋 Initial Assessment** 
   - Answer 5 AI-generated questions
   - View inline feedback for each answer
   - Automatic level determination
5. **🚀 Personalized Learning Path**
   - Auto-generated based on assessment results
   - Sequenced lessons tailored to student level
   - Adaptive content difficulty
6. **📖 Structured Learning**
   - Study concept explanations
   - Review real-world examples
   - Complete practice quizzes
   - Track completion status
7. **📊 Dashboard & Analytics**
   - View performance metrics
   - Track progress across concepts
   - Monitor mastery levels

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │ (app.py)
│  (Main Entry)   │
└────────┬────────┘
         │
    ┌────▼─────┬──────────────┬────────────────┬──────────────┐
    │           │              │                │              │
┌───▼──────┐ ┌─▼───────────┐ ┌▼─────────────┐ ┌▼────────────┐
│ Login &  │ │ Assessment  │ │  Learning    │ │  Knowledge │
│ Profile  │ │   Flow      │ │  Path Gen    │ │  Tracing   │
└──────────┘ └─────────────┘ └──────────────┘ └────────────┘
    │            │                  │                │
    └────────────┴──────────────────┴────────────────┘
              │
    ┌─────────▼─────────┐
    │  GroqAI Engine    │
    │  (groq_ai.py)     │
    └───────────────────┘
              │
         Groq API
      (Cloud-based LLM)
```

### Component Details

- **tutor_agent.py** - Main AI tutor orchestrator
- **groq_ai.py** - Groq API integration and prompt engineering
- **learner_profiling.py** - Student profile management and knowledge vectors
- **knowledge_tracing.py** - Simplified DKT for mastery estimation
- **learning_path.py** - Generates adaptive learning sequences
- **adaptive_quiz.py** - Question generation and difficulty adaptation
- **evaluation.py** - Performance metrics and analytics
- **courses.py** - Course definitions and structure
- **curriculum.py** - Curriculum management
- **learning_content.py** - Content generation and recommendations
- **structured_learning.py** - Structured learning session management

## 📁 Project Structure

```
PersonalizedTutorAgent/
├── app.py                              # Main Streamlit application
├── settings.json                       # Configuration (API keys, models)
├── requirements.txt                    # Python dependencies
├── INSTALLATION.md                     # Detailed setup guide
├── README.md                           # This file
├── data/
│   ├── student_interactions.csv        # Student performance history
│   └── question_bank.csv               # Question database
└── src/
    ├── __init__.py
    ├── tutor_agent.py                  # Core AI tutor agent
    ├── groq_ai.py                      # Groq API client
    ├── config.py                       # Configuration loader
    ├── adaptive_quiz.py                # Quiz engine & difficulty adaptor
    ├── learner_profiling.py            # Student profile management
    ├── knowledge_tracing.py            # DKT mastery model
    ├── learning_path.py                # Adaptive path generation
    ├── learning_content.py             # Content orchestration
    ├── evaluation.py                   # Performance metrics
    ├── courses.py                      # Course definitions
    ├── curriculum.py                   # Curriculum management
    ├── structured_learning.py          # Structured learning flow
    ├── __pycache__/                    # Python cache
    └── archive/                        # Backup/old code
        ├── template_based_tutor_agent.py
        └── tutor_agent_backup.py
```

## 🔧 Configuration

Edit `settings.json` to configure the application:

```json
{
  "groq_api_key": "gsk_YOUR_API_KEY_HERE",
  "groq_model": "llama-3.3-70b-versatile",
  "response_timeout": 30,
  "retry_attempts": 3,
  "log_ai_calls": true
}
```

### Configuration Options

- **groq_api_key** - Your Groq API key (get from console.groq.com)
- **groq_model** - LLM model to use (default: llama-3.3-70b-versatile)
- **response_timeout** - API response timeout in seconds
- **retry_attempts** - Number of retries for failed API calls
- **log_ai_calls** - Enable/disable API call logging

## 🚀 Getting Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for free account (no credit card required)
3. Navigate to API Keys section
4. Create new API key
5. Copy the key and paste into `settings.json` under `groq_api_key`

## 📚 How It Works

### Initial Assessment Process

1. User answers **5 progressive questions**:
   - Question 1: Easy
   - Question 2: Easy-Medium
   - Question 3: Medium
   - Question 4: Medium-Hard
   - Question 5: Hard

2. **Inline Feedback** appears after each answer:
   - Shows if answer is correct/incorrect
   - Displays the correct answer
   - Provides detailed explanation
   - User clicks "Next Question" to continue

3. **Level Determination**:
   - Score 0-2/5 → Beginner level
   - Score 3/5 → Intermediate level
   - Score 4-5/5 → Advanced level

4. **Automatic Learning Path Generation**:
   - Creates personalized sequence based on level
   - Recommends concepts to study
   - Adapts difficulty to student needs

### Learning Path Structure

Each learning session includes:
- **Concept Explanation** - AI-generated detailed explanation
- **Real Examples** - Practical examples demonstrating the concept
- **Practice Quiz** - Questions to test understanding
- **Progress Tracking** - Shows completion status

### Knowledge Tracing

System tracks:
- Correct/incorrect responses per concept
- Estimated mastery level (0-1.0)
- Learning trajectory over time
- Gaps in understanding

## 🎯 Supported Subjects

- **Mathematics**
- **Physics**
- **Chemistry**

(More subjects can be added in `courses.py`)

## 📊 Example Assessment Flow

```
User logs in
    ↓
Selects Subject (e.g., Mathematics)
    ↓
Selects Course (e.g., Algebra)
    ↓
Takes 5-question assessment
    ├─ Q1 (Easy): User answers → Inline feedback
    ├─ Q2 (Easy-Med): User answers → Inline feedback
    ├─ Q3 (Medium): User answers → Inline feedback
    ├─ Q4 (Med-Hard): User answers → Inline feedback
    └─ Q5 (Hard): User answers → Inline feedback
    ↓
System calculates: Score 4/5 → Advanced level
    ↓
Generates 10-concept learning path
    ↓
Starts Structured Learning
    ├─ Concept 1: Explanation → Examples → Quiz
    ├─ Concept 2: Explanation → Examples → Quiz
    └─ ... continues
```

## 🔌 API Integration

Uses **Groq API** for:
- Question generation
- Answer evaluation
- Explanation generation
- Learning path recommendations
- Content generation

**Why Groq?**
- High-speed inference (70B+ token/sec)
- Free tier available
- Excellent for educational applications
- No rate limiting during free usage

## 📈 Performance Metrics

Track student progress through:
- **Accuracy Rate** - % of questions answered correctly
- **Mastery Score** - Estimated knowledge level per concept (0-100%)
- **Learning Velocity** - Speed of improvement
- **Time Spent** - Duration per concept
- **Attempts** - Number of retries per question

## 🛠️ Technology Stack

- **Frontend** - Streamlit (Python web UI)
- **AI Engine** - Groq API (llama-3.3-70b)
- **Backend** - Python 3.8+
- **Data Storage** - CSV (expandable to database)
- **ML Models** - Simplified DKT, Knowledge Vectors
- **Visualization** - Plotly, Matplotlib

## ✨ Key Improvements (Latest Version)

- **5-Question Assessment** (upgraded from 3)
- **Inline Feedback System** - No separate review page
- **Automatic Learning Path Generation** - Direct flow from assessment
- **Progressive Difficulty** - 5-level difficulty progression
- **Structured Learning Flow** - Multi-step learning format
- **Real-time Performance Tracking** - Immediate feedback and metrics

## 🐛 Troubleshooting

**Issue: "API key not found"**
- Ensure `settings.json` has valid `groq_api_key`
- Get key from https://console.groq.com

**Issue: "Questions not generating"**
- Check internet connection to Groq API
- Verify API key is valid and active
- Check `response_timeout` setting

**Issue: "Port 8501 already in use"**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

## 📝 License

This project is part of an educational AI tutoring system.

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional subjects/courses
- More ML models for knowledge tracing
- Enhanced analytics dashboard
- Mobile app support
- Offline functionality

## 📧 Support

For issues or questions, check:
1. INSTALLATION.md for setup problems
2. settings.json for configuration
3. Groq console for API key verification

---

**Happy Learning! 🚀**

**Free tier benefits:**
- 30 requests/minute
- Unlimited requests/day
- All models available
- No credit card required

## 🧠 How AI Works

### Question Generation
- Groq AI creates unique questions for each concept
- Generates 4 plausible options with one correct answer
- Automatically determines the correct answer
- Provides explanation for why answer is correct

### Adaptive Difficulty
- **Easy**: When accuracy < 50%
- **Medium**: When accuracy 50-80%
- **Hard**: When accuracy > 80%

### Feedback Generation
- Explains why answers are correct/incorrect
- Provides helpful hints when requested
- Suggests next learning steps
- Offers motivational messages

## 📦 Requirements

- Python 3.8+
- Streamlit 1.28.0+
- Pandas, NumPy
- Groq API (free account)

## 💡 Key Concepts

### Learner Profiling
Tracks student performance across concepts:
- Accuracy per concept
- Attempt history
- Time spent
- Current mastery level

### Knowledge Tracing
Predicts student understanding using Simplified Bayesian Knowledge Tracing:
- Estimates P(knows concept)
- Predicts next question outcome
- Tracks learning trajectory

### Adaptive Learning Paths
Personalized concept sequences:
- Orders by priority and prerequisites
- Respects learning science principles
- Adjusts based on performance

### Adaptive Quiz Engine
Difficulty-adjusting questions:
- Selects questions matching student level
- Changes difficulty based on performance
- Provides immediate feedback

## 🔄 Complete User Journey

```
1. Login
   ↓
2. Select Subject (Math, Science, History, etc.)
   ↓
3. Initial Assessment (3 questions)
   • Easy question
   • Medium question
   • Hard question
   ↓
4. Determine Level (Beginner/Intermediate/Advanced)
   ↓
5. Choose Activity
   ├── Interactive Quiz (adaptive)
   ├── Dashboard (view progress)
   ├── Learning Path (concept sequence)
   └── Analytics (detailed metrics)
   ↓
6. Receive AI Feedback
   • Immediate response evaluation
   • Explanation of correct answer
   • Hints for improvement
   • Next recommended concept
```

## 🎯 Core Modules

| Module | Purpose | Key Classes |
|--------|---------|------------|
| `tutor_agent.py` | AI feedback & guidance | PersonalizedTutorAgent |
| `groq_ai.py` | Groq API integration | GroqAITutor |
| `learner_profiling.py` | Student tracking | LearnerProfile, LearnerProfileManager |
| `knowledge_tracing.py` | Mastery prediction | SimplifiedDKT |
| `learning_path.py` | Concept sequencing | LearningPathGenerator, AdaptivePathManager |
| `adaptive_quiz.py` | Question selection | QuestionBank, AdaptiveQuizEngine, DifficultyAdaptor |
| `evaluation.py` | Performance metrics | Various evaluators |

## 📊 Data Files

### `student_interactions.csv`
Stores student responses:
- student_id: Student identifier
- concept: Learning topic
- question_id: Question number
- correct: 1 if correct, 0 if incorrect
- time_spent: Time in seconds
- timestamp: When answered

### `question_bank.csv`
Question database:
- question_id: Unique identifier
- concept: Topic covered
- difficulty: Easy/Medium/Hard
- bloom_level: Cognitive level
- avg_solve_time: Average time needed

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Server Deployment
```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8080
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn --workers 4 app:app
```

## ❓ Troubleshooting

**Q: "API key not found"**
A: Check `settings.json` has your key from console.groq.com

**Q: "Questions not showing"**
A: Verify internet connection and API key validity

**Q: "Streamlit not found"**
A: Run `pip install -r requirements.txt`

See [INSTALLATION.md](INSTALLATION.md) for more troubleshooting.

## 📚 Learn More

- [Streamlit Documentation](https://docs.streamlit.io)
- [Groq API Documentation](https://console.groq.com/docs)
- [Deep Knowledge Tracing Paper](https://arxiv.org/abs/1506.05908)
- [Intelligent Tutoring Systems](https://en.wikipedia.org/wiki/Intelligent_tutoring_system)

## 📝 Notes

- All questions are AI-generated dynamically
- Student responses auto-graded by AI
- No hardcoded templates - pure AI-driven
- Data stored locally in CSV format
- Can be extended with database backend

## ✨ Future Enhancements

- Real-time collaborative learning
- Mobile application
- LSTM-based Deep Knowledge Tracing
- Transformer-based NLP feedback
- Reinforcement learning for sequencing

## 🚀 Roadmap

### Phase 1: Core Enhancements (March 2026)
- **Course Management System**:
  - Implement `courses.py` to manage course catalog.
  - Add course selection UI in `app.py`.
  - Filter questions and learning paths by selected course.
  - Track student progress per course.
- **Learning Analytics Dashboard**:
  - Visualize student performance (heatmaps, timelines).
  - Add concept mastery radar charts.
  - Identify weak concepts dynamically.

### Phase 2: Advanced Features (April 2026)
- **AI-Powered Question Generator**:
  - Integrate Groq AI to auto-generate questions.
  - Support Bloom's taxonomy levels.
  - Validate generated questions with AI feedback.
- **Dynamic Learning Paths**:
  - Enhance `learning_path.py` to adapt paths in real-time.
  - Include course prerequisites in path generation.

### Phase 3: Scalability & Optimization (May 2026)
- **Database Integration**:
  - Migrate from CSV/JSON to SQLite/PostgreSQL.
  - Optimize data queries for large datasets.
- **Performance Improvements**:
  - Refactor code for faster API calls.
  - Add caching for frequently accessed data.

### Phase 4: Deployment & User Feedback (June 2026)
- **Deployment**:
  - Deploy on cloud (AWS/GCP/Heroku).
  - Add CI/CD pipelines for automated testing.
- **User Feedback**:
  - Collect feedback from students and educators.
  - Iterate on features based on feedback.

---

This roadmap provides a structured plan for enhancing the Personalized Tutor Agent. Each phase builds on the previous, ensuring steady progress and scalability.
