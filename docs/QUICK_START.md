# ⚡ 30-Minute Quick Start Guide
## Get Personalized Tutor Agent Running Fast!

For a **complete detailed guide**, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

## Prerequisites Check (2 minutes)

Before starting, you need:
- [ ] Windows, Mac, or Linux
- [ ] 2 GB free disk space
- [ ] Internet connection

---

## 🪟 Windows Users - 30 Minutes

### Option 1: Automated Setup (Easiest) ⭐
1. **Download and Extract** the project folder
2. **Double-click** `setup_windows.bat`
3. **Wait** for setup to complete
4. **Done!** Run: `python run_pipeline.py`

### Option 2: Manual Setup
**5 minutes - Install Requirements**
1. Install Python 3.8+: https://www.python.org/downloads/
   - ⚠️ **Check "Add Python to PATH"**
2. Install Git: https://git-scm.com/download/win
3. Verify: Open Command Prompt
   ```bash
   python --version
   ```

**10 minutes - Download Project**
1. Open Command Prompt/PowerShell
2. Go to desired folder: `cd Documents`
3. Clone: `git clone <repo-url>`
4. Navigate: `cd PersonalizedTutorAgent`

**10 minutes - Setup & Install**
1. Create virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**5 minutes - Run**
```bash
python run_pipeline.py
streamlit run app.py
```

**What you'll see:**
1. Pipeline runs for 2-5 minutes
2. Dashboard opens at `http://localhost:8501`
3. Explore the 5 tabs: Dashboard, Quiz, Learning Path, Analytics, System Info

---

## 🍎 Mac Users - 30 Minutes

### Fastest Method:
```bash
# 1. Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Git & Python
brew install git python3

# 3. Clone project
git clone <repo-url>
cd PersonalizedTutorAgent

# 4. Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Run
python3 run_pipeline.py
streamlit run app.py
```

---

## 🐧 Linux Users - 30 Minutes

### Ubuntu/Debian:
```bash
# 1. Install dependencies
sudo apt update
sudo apt install git python3 python3-pip python3-venv

# 2. Clone project
git clone <repo-url>
cd PersonalizedTutorAgent

# 3. Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Run
python3 run_pipeline.py
streamlit run app.py
```

### Fedora/RHEL:
```bash
# 1. Install dependencies
sudo dnf install git python3 python3-pip

# 2-4. Same as Ubuntu above
```

---

## ✅ Verify Installation (2 minutes)

After setup, test each component:

```bash
# Check Python
python --version           # Should be 3.8+

# Check pip packages
pip list                   # Should show pandas, numpy, etc.

# Check virtual env is active
# Should see (venv) in your prompt
```

---

## 🚀 Run the System (5 minutes)

### Step 1: Generate Data & Run Pipeline
```bash
python run_pipeline.py
```

Expected output:
```
✓ Dataset generated successfully!
✓ Learner profiles created!
✓ DKT model initialized!
✓ Learning path generator initialized!
✓ Quiz engine initialized!
✓ Tutor agent initialized!
✓ Evaluation report generated!
✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!
```

### Step 2: Launch Streamlit Interactive Dashboard
```bash
streamlit run app.py
```

**What to expect:**
1. Streamlit initializes
2. Browser **opens automatically** at `http://localhost:8501`
3. **Personalized Tutor Agent Dashboard** loads 🎉

**If browser doesn't open:**
- Copy URL from terminal: `http://localhost:8501`
- Paste into your browser address bar
- Press Enter

### Step 3: Explore the Dashboard
Once the dashboard loads, you'll see 5 main tabs:
- **📊 Dashboard Tab**: Overall system metrics and status
- **📝 Interactive Quiz Tab**: Take adaptive quizzes with difficulty control
- **🛤️ Learning Path Tab**: View your personalized learning sequence
- **📈 Analytics Tab**: Detailed performance metrics and visualizations
- **ℹ️ System Info Tab**: Project information and technical details

### Step 4: Stop Dashboard (When Done)
```bash
Ctrl + C  # Hold Ctrl and press C
# Type: y (or just press Enter)
```

---

## 📦 What Gets Installed (Understanding dependencies)

The `requirements.txt` includes:
- **streamlit** (1.28.0) ⭐ - Web app framework for dashboard
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scikit-learn** - Machine learning
- **plotly** - Interactive charts
- **scipy** - Scientific computing
- **matplotlib & seaborn** - Data visualization

All installed automatically with: `pip install -r requirements.txt`

---

## 🎯 Common Issues & Quick Fixes

| Problem | Solution |
|---------|----------|
| `python not found` | Install Python with "Add to PATH" checked |
| `pip not found` | Reinstall Python, check PATH |
| `(venv) not showing` | Activate: `.\venv\Scripts\Activate.ps1` (Win) |
| `Module not found` | Run: `pip install -r requirements.txt` again |
| `streamlit not found` | Run: `pip install streamlit==1.28.0` |
| Dashboard won't open | Wait 10 seconds, check `http://localhost:8501` |
| Port 8501 in use | Run: `streamlit run app.py --server.port 8502` |
| Dashboard blank/error | Stop (Ctrl+C), run pipeline again, restart |

For more issues, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md#troubleshooting)

---

## 📚 Next Steps

After successful installation:

1. **Read Documentation**
   - See [README.md](../README.md) for complete guide
   - Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for examples
   - Review [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) for detailed steps

2. **Explore Code**
   - Look at `src/` modules
   - Read `run_pipeline.py` to understand workflow
   - Check `app.py` for dashboard code

3. **Customize**
   - Modify dataset parameters in `data/generate_synthetic_data.py`
   - Adjust DKT settings in `src/knowledge_tracing.py`
   - Add new concepts in the data files

---

## 🆘 Need Help?

1. **Installation issues?** → See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md#troubleshooting)
2. **How to use?** → See [README.md](README.md)
3. **Code examples?** → See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
4. **System architecture?** → See `reports/architecture.py`
5. **Research details?** → See `reports/research_report_generator.py`

---

## 💡 What's Happening Behind the Scenes?

When you run `python run_pipeline.py`:

1. **Generates** 50 student profiles
2. **Creates** 3,000 learning interactions
3. **Trains** a knowledge tracing model
4. **Builds** personalized learning paths
5. **Evaluates** system performance
6. **Creates** reports and visualizations

When you run `streamlit run app.py`:

1. **Loads** all student data
2. **Provides** interactive dashboard
3. **Enables** quiz taking
4. **Shows** learning analytics
5. **Displays** system information

---

## 🎓 You're Ready!

**Congratulations!** Your Personalized Tutor Agent is installed and running! 🎉

### Quick Commands Reference:
```bash
# Activate environment
.\venv\Scripts\Activate.ps1          # Windows
source venv/bin/activate              # Mac/Linux

# Run system
python run_pipeline.py                 # Generate data & run

# Launch dashboard
streamlit run app.py                   # Interactive interface

# Deactivate environment
deactivate                             # When done

# Install more packages
pip install <package-name>             # Add new dependencies
```

---

**Have fun exploring the system! Happy learning! 🚀**
