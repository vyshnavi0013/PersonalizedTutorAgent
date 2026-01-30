# 🎓 Personalized Tutor Agent

An AI-powered Intelligent Tutoring System with Groq AI integration for personalized learning.

## ⚡ Quick Start

### Installation
For detailed step-by-step installation guide, see [INSTALLATION.md](INSTALLATION.md)

**Quick version:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add API key to settings.json
# Get key from https://console.groq.com (free)

# 3. Run application
streamlit run app.py
```

## 🌟 Features

- **AI-Powered Questions**: Groq AI generates custom questions dynamically
- **Adaptive Difficulty**: Questions adjust based on student performance
- **Auto-Grading**: AI determines correct answers and validates responses
- **Personalized Feedback**: AI-generated explanations and hints
- **Initial Assessment**: 3-question diagnostic to determine student level
- **Interactive Quiz**: Adaptive quiz with real-time AI feedback
- **Learning Analytics**: Track progress and mastery

## 📊 User Flow

1. **Login/Register** - Create student account
2. **Select Subject** - Choose learning topic
3. **Initial Assessment** - 3 AI-generated questions (Easy → Medium → Hard)
4. **Dashboard** - View knowledge state and learning progress
5. **Interactive Quiz** - Practice with adaptive difficulty
6. **Analytics** - Review performance metrics

## 🏗️ Architecture

```
app.py (Streamlit UI)
├── PersonalizedTutorAgent (tutor_agent.py)
│   └── GroqAITutor (groq_ai.py) ← AI Engine
├── LearnerProfileManager (learner_profiling.py)
├── SimplifiedDKT (knowledge_tracing.py)
├── AdaptivePathManager (learning_path.py)
└── QuestionBank (adaptive_quiz.py)

Data
├── student_interactions.csv
└── question_bank.csv
```

## 📁 Project Structure

```
PersonalizedTutorAgent/
├── app.py                         # Main Streamlit application
├── settings.json                  # Configuration (API keys)
├── requirements.txt               # Dependencies
├── INSTALLATION.md                # Installation guide
├── README.md                      # This file
├── data/
│   ├── student_interactions.csv   # Student performance data
│   └── question_bank.csv          # Question database
└── src/
    ├── tutor_agent.py             # Main AI tutor agent
    ├── groq_ai.py                 # Groq API integration
    ├── config.py                  # Configuration loader
    ├── adaptive_quiz.py            # Quiz engine & difficulty adaptor
    ├── learner_profiling.py        # Student profile & tracking
    ├── knowledge_tracing.py        # DKT model for mastery prediction
    ├── learning_path.py            # Adaptive path generation
    ├── evaluation.py               # Performance metrics
    └── archive/                    # Archived backup code
```

## 🔧 Configuration

Edit `settings.json` to configure:

```json
{
  "groq_api_key": "gsk_...",           # Get from console.groq.com
  "groq_model": "llama-3.3-70b-versatile",
  "response_timeout": 30,              # API timeout in seconds
  "retry_attempts": 3,                 # Number of retries
  "log_ai_calls": true                 # Enable API logging
}
```

## 🚀 Getting Your API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free, no credit card needed)
3. Create an API key
4. Copy and paste into `settings.json`

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

## 📄 License

Educational project for research and learning purposes.

---

**For installation help:** See [INSTALLATION.md](INSTALLATION.md)

**Last Updated**: January 2026
**Status**: Production Ready ✅
