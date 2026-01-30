# Installation Guide

Complete step-by-step guide to install and run the Personalized Tutor Agent on a new device.

## Prerequisites

Before you start, ensure you have:

- **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Git** (optional, for cloning) - [Download from git-scm.com](https://git-scm.com/)
- **Groq API Key** (free) - [Get from console.groq.com](https://console.groq.com)

## Step 1: Get the Code

### Option A: Clone from Git (Recommended)
```bash
git clone <repository-url>
cd PersonalizedTutorAgent
```

### Option B: Manual Download
1. Download the project as ZIP
2. Extract to desired location
3. Open terminal in that folder

## Step 2: Create Virtual Environment (Recommended)

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

**Note**: You'll see `(venv)` prefix in terminal when activated.

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web interface
- `pandas` - Data handling
- `numpy` - Numerical computing
- `groq` - AI API client
- `plotly` - Visualizations

**Installation takes 2-3 minutes.**

## Step 4: Get Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Click "Sign Up" (or "Sign In" if you have account)
3. Create a free account
4. Navigate to "API Keys"
5. Click "Create API Key"
6. Copy the key (starts with `gsk_`)

**Free tier includes:**
- 30 requests per minute
- Unlimited requests per day
- Access to all models
- No credit card needed

## Step 5: Configure Settings

Open `settings.json` in your text editor and paste your API key:

```json
{
  "groq_api_key": "gsk_YOUR_KEY_HERE",
  "groq_model": "llama-3.3-70b-versatile",
  "response_timeout": 30,
  "retry_attempts": 3,
  "log_ai_calls": true
}
```

**Replace** `gsk_YOUR_KEY_HERE` with your actual API key.

### Example:
```json
{
  "groq_api_key": "gsk_9K3jD2L8mP0qR5sT7uV9wX1yZ3aB5cD7",
  "groq_model": "llama-3.3-70b-versatile",
  "response_timeout": 30,
  "retry_attempts": 3,
  "log_ai_calls": true
}
```

## Step 6: Run the Application

```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open your browser and go to `http://localhost:8501`

## Step 7: Test the Application

1. **Login** - Create a test account (any email/password works)
2. **Select Subject** - Choose a learning topic
3. **Initial Assessment** - Answer 3 AI-generated questions
4. **Interactive Quiz** - Start practicing
5. **Dashboard** - View your progress

If you see **AI-generated questions**, setup is successful! ✅

## Directory Structure

After installation, your folder should look like:

```
PersonalizedTutorAgent/
├── app.py                    # Main application
├── settings.json             # Configuration
├── requirements.txt          # Dependencies
├── INSTALLATION.md           # This file
├── README.md                 # Project overview
├── data/
│   ├── question_bank.csv     # Question data
│   └── student_interactions.csv  # Student data
└── src/
    ├── tutor_agent.py        # AI tutor
    ├── groq_ai.py            # Groq API
    ├── config.py             # Config loader
    ├── adaptive_quiz.py       # Quiz engine
    ├── learner_profiling.py   # Student tracking
    ├── knowledge_tracing.py   # Learning model
    ├── learning_path.py       # Path generation
    ├── evaluation.py          # Metrics
    └── archive/              # Backup files
```

## Troubleshooting

### Problem: "Python not found"
**Solution:**
- Download Python from [python.org](https://python.org)
- During installation, check "Add Python to PATH"
- Restart terminal and try again

### Problem: "No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit
```

### Problem: "API key not found"
**Solution:**
1. Check `settings.json` exists in project root
2. Verify `groq_api_key` is present
3. Check key format: starts with `gsk_`
4. Verify no extra spaces or quotes

### Problem: "Connection refused" or "Failed to connect to API"
**Solution:**
1. Check internet connection
2. Verify Groq API status: [status.groq.com](https://status.groq.com)
3. Wait 1 minute and try again (rate limit)
4. Check firewall isn't blocking Groq domain

### Problem: "streamlit: command not found" on Mac/Linux
**Solution:**
```bash
# Activate virtual environment first
source venv/bin/activate

# Then run
streamlit run app.py
```

### Problem: Questions not showing in quiz
**Solution:**
1. Check API key is valid
2. Check internet connection
3. Wait a moment (AI is generating)
4. Check browser console for errors (F12)

## Configuration Options

Edit `settings.json` to customize:

```json
{
  "groq_api_key": "gsk_...",           // Required: Your API key
  "groq_model": "llama-3.3-70b-versatile",  // AI model
  "response_timeout": 30,              // API timeout (seconds)
  "retry_attempts": 3,                 // Number of retries
  "log_ai_calls": true                 // Enable logging
}
```

## Running on Different Ports

Default port is 8501. To use a different port:

```bash
streamlit run app.py --server.port=8080
```

## Running on Server/Cloud

### For remote access:
```bash
streamlit run app.py --server.address=0.0.0.0
```

Then access from: `http://<server-ip>:8501`

### For production (with gunicorn):
```bash
pip install gunicorn
gunicorn --workers 4 --threads 2 --worker-class=gthread --bind=0.0.0.0:8000 app:app
```

## Deactivating Virtual Environment

When done working:

```bash
deactivate
```

## Updating Dependencies

To update packages to latest versions:

```bash
pip install -r requirements.txt --upgrade
```

## Uninstalling

To remove the application:

### On Windows:
```bash
# Deactivate virtual environment
venv\Scripts\deactivate

# Delete the folder
rmdir /s PersonalizedTutorAgent
```

### On Mac/Linux:
```bash
# Deactivate virtual environment
deactivate

# Delete the folder
rm -rf PersonalizedTutorAgent
```

## What to Do Next

1. **Explore Features** - Try login, quiz, dashboard
2. **Customize Questions** - Edit `data/question_bank.csv`
3. **Modify Settings** - Adjust API configuration
4. **Integrate Data** - Use your own student data

## Getting Help

- **Groq API Issues**: [Groq Docs](https://console.groq.com/docs)
- **Streamlit Issues**: [Streamlit Docs](https://docs.streamlit.io)
- **Python Issues**: [Python Docs](https://docs.python.org)

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.10+ |
| RAM | 2GB | 4GB+ |
| Disk | 500MB | 1GB+ |
| Internet | Required | Broadband |

## Next Steps

After successful installation:

1. ✅ Application is running
2. ✅ API is configured
3. 📝 Read [README.md](README.md) for features
4. 🎓 Start learning with the app
5. 🔧 Customize as needed

---

**Installation Time**: 10-15 minutes
**Difficulty**: Beginner-friendly
**Support**: Check troubleshooting section above
