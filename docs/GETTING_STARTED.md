# 🎯 Getting Started - Choose Your Path

Welcome to **Personalized Tutor Agent**! This document helps you choose the right installation guide for your situation.

---

## 🚦 Which Guide Should I Follow?

### 👨‍💻 I'm a Complete Beginner (New to Python/Git/etc)
→ **[QUICK_START.md](QUICK_START.md)** ⭐

- 30-minute quick setup
- Step-by-step instructions
- Automated setup options
- Troubleshooting guide

**Best for:** First-time users, non-programmers, just want it working fast

---

### 📚 I Want Detailed, Thorough Instructions
→ **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)**

- Complete system requirements
- Detailed steps for each OS (Windows, Mac, Linux)
- Explanations of what each step does
- Comprehensive troubleshooting
- Verification checklist

**Best for:** Detailed learners, want to understand the process, prefer full documentation

---

### ⚡ I Just Want to Get It Running (Experienced Users)
→ **Use Automated Setup:**

**Windows:**
```bash
setup_windows.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Best for:** Experienced developers, familiar with Python/Git

---

### 📖 I Want Complete Project Documentation
→ **[README.md](README.md)**

Complete technical documentation including:
- Module documentation
- API references
- Architecture overview
- Usage examples
- Advanced configuration

**Best for:** Understanding the system deeply, using as reference

---

## 🎬 Quick Setup (2 Minutes)

### What You Need:
- [ ] Python 3.8 or higher
- [ ] Git
- [ ] 2 GB disk space
- [ ] Internet connection

### Windows Users:
```bash
# Option 1: Automated (Easiest)
setup_windows.bat

# Option 2: Manual
git clone <repo-url>
cd PersonalizedTutorAgent
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run_pipeline.py
streamlit run app.py
```

### Mac/Linux Users:
```bash
# Option 1: Automated (Easiest)
chmod +x setup.sh
./setup.sh

# Option 2: Manual
git clone <repo-url>
cd PersonalizedTutorAgent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run_pipeline.py
streamlit run app.py
```

---

## 📋 Installation Checklist

Before you start, verify you have:

- [ ] **Python installed** (version 3.8+)
  - Check: Open terminal/command prompt
  - Type: `python --version`
  - Should show: `Python 3.8` or higher

- [ ] **Git installed**
  - Check: `git --version`
  - Should show a version number

- [ ] **Internet connection**
  - For downloading dependencies
  - For cloning the repository

- [ ] **Administrator access (Windows)**
  - May be needed for installation

- [ ] **At least 2 GB free disk space**

---

## ⚠️ Common Mistakes to Avoid

1. **Not installing Python** ← Most common error
   - Go to https://www.python.org/downloads/
   - Download and install

2. **Not checking "Add Python to PATH"** (Windows)
   - When installing Python, check this box!
   - If missed, reinstall Python

3. **Not activating virtual environment**
   - Windows: `.\venv\Scripts\Activate.ps1`
   - Mac/Linux: `source venv/bin/activate`
   - You should see `(venv)` in your prompt

4. **Using `python` instead of `python3`** (Mac/Linux)
   - Mac/Linux requires: `python3`, not `python`

5. **Not being in the project directory**
   - Use: `cd PersonalizedTutorAgent` first
   - Then run commands

---

## 🎯 5-Step Installation Overview

### Step 1: Install Software (5-10 minutes)
- [ ] Python 3.8+
- [ ] Git

### Step 2: Clone Repository (2 minutes)
```bash
git clone <repo-url>
cd PersonalizedTutorAgent
```

### Step 3: Create Virtual Environment (2 minutes)
```bash
python -m venv venv  # Windows
python3 -m venv venv  # Mac/Linux
```

### Step 4: Activate Environment (1 minute)
```bash
.\venv\Scripts\Activate.ps1  # Windows PowerShell
.\venv\Scripts\activate.bat  # Windows CMD
source venv/bin/activate      # Mac/Linux
```

### Step 5: Install Dependencies (5-10 minutes)
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the System

### Generate Data & Run Pipeline (2-5 minutes):
```bash
python run_pipeline.py
```

Expected output:
```
✓ Dataset generated successfully!
✓ Learner profiles created!
✓ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!
```

### Launch Interactive Dashboard (1 minute):
```bash
streamlit run app.py
```

Browser opens automatically → Dashboard displays! 🎉

---

## 🆘 Something Went Wrong?

### Common Issues & Solutions:

**"Python not found"**
- Install Python from https://www.python.org/
- Make sure "Add Python to PATH" is checked

**"Module not found"**
- Verify virtual environment is active (see `(venv)` in prompt)
- Run: `pip install -r requirements.txt` again

**"Permission denied" (Mac/Linux)**
- Run: `chmod +x setup.sh`
- Then: `./setup.sh`

**"Port already in use"**
- Run: `streamlit run app.py --server.port 8502`

**Virtual environment won't activate (Windows)**
- Run PowerShell as Administrator
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Try activation again

For more issues, see [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md#troubleshooting)

---

## 📚 Documentation Files

| File | Purpose | For Whom |
|------|---------|----------|
| [QUICK_START.md](QUICK_START.md) | 30-minute quick setup | Beginners |
| [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) | Detailed step-by-step | Detailed learners |
| [README.md](README.md) | Complete documentation | Everyone |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Code examples | Developers |
| [INDEX.md](INDEX.md) | File & content index | Navigation |
| [setup_windows.bat](setup_windows.bat) | Automated setup | Windows users |
| [setup.sh](setup.sh) | Automated setup | Mac/Linux users |

---

## ✅ Success Indicators

After installation, you'll know it's working when:

1. ✅ You see `(venv)` in your command prompt
2. ✅ `python --version` shows 3.8+
3. ✅ `pip list` shows pandas, numpy, streamlit, etc.
4. ✅ `python run_pipeline.py` runs without errors
5. ✅ Dashboard opens when you run `streamlit run app.py`

---

## 🎓 What Happens Next?

After successful installation:

1. **Read documentation** → [README.md](README.md)
2. **Explore the code** → Check `src/` folder
3. **See examples** → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
4. **Understand design** → `reports/architecture.py`
5. **Customize** → Modify parameters in config files

---

## 🚀 Ready to Start?

### Choose your path:

1. **New to programming?** → [QUICK_START.md](QUICK_START.md)
2. **Want detailed guide?** → [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
3. **Experienced user?** → Run `setup_windows.bat` or `setup.sh`
4. **Understanding code?** → [README.md](README.md)

---

## 💬 Need Help?

1. Check [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md#troubleshooting) troubleshooting section
2. Review [QUICK_START.md](QUICK_START.md#-common-issues--quick-fixes) common issues
3. Look at file comments in source code
4. Check [README.md](README.md) for API documentation

---

## 🎉 You've Got This!

**Installation is straightforward.** Follow one of the guides above, and you'll have the system running in 30 minutes or less!

**Good luck! Happy learning! 🚀**

---

**Questions?** Start with the appropriate guide above:
- Beginner? → [QUICK_START.md](QUICK_START.md)
- Detailed? → [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- Deep dive? → [README.md](README.md)
