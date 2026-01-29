# 🚀 Complete Installation Guide
## Personalized Tutor Agent - Step by Step Setup

### For Complete Beginners - No Prior Experience Needed!

This guide will walk you through every step to get the Personalized Tutor Agent running on your computer.

---

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [Mac Installation](#mac-installation)
4. [Linux Installation](#linux-installation)
5. [Troubleshooting](#troubleshooting)
6. [Verification Checklist](#verification-checklist)

---

## System Requirements

### Minimum Requirements
- **Hard Disk Space**: 2 GB free space
- **RAM**: 4 GB minimum (8 GB recommended)
- **Internet Connection**: Required for downloading dependencies
- **Operating System**: Windows 7+, macOS 10.14+, or Linux (Ubuntu 18.04+)

### What You'll Need
- Git (for cloning the repository)
- Python 3.8 or higher
- pip (Python package manager - comes with Python)

---

# 🪟 WINDOWS INSTALLATION GUIDE

## Step 1: Install Git

### 1.1 Download Git
1. Go to https://git-scm.com/download/win
2. Click on **"Click here to download manually"** or wait for automatic download
3. A file named `Git-X.XX.X-64-bit.exe` will download (size ~50MB)

### 1.2 Install Git
1. Double-click the downloaded `.exe` file
2. Click **"Yes"** when asked for permission
3. Read the license and click **"Next"**
4. Select installation location (default is fine) → **"Next"**
5. On "Select Components" → **"Next"** (keep defaults)
6. On "Select Start Menu Folder" → **"Next"**
7. On "Choose the default editor used by Git" → **"Next"**
8. On "Adjust your PATH environment" → Select **"Git from the command line..."** → **"Next"**
9. On "Choose HTTPS transport backend" → **"Next"**
10. On "Configure line ending conversions" → **"Next"**
11. On "Configure terminal emulator" → **"Next"**
12. On "Choose default behavior of 'git pull'" → **"Next"**
13. On "Choose a credential helper" → **"Next"**
14. On "Configure extra options" → **"Next"**
15. On "Configure experimental options" → **"Install"**
16. Wait for installation to complete → **"Finish"**

### 1.3 Verify Git Installation
1. Open **Command Prompt** or **PowerShell**:
   - Right-click on desktop
   - Select **"Open PowerShell here"** or **"Command Prompt here"**
2. Type this command and press Enter:
   ```bash
   git --version
   ```
3. You should see: `git version X.XX.X` (version number)
   - ✅ If you see version: Git is installed correctly
   - ❌ If you see "not recognized": Restart your computer and try again

---

## Step 2: Install Python

### 2.1 Download Python
1. Go to https://www.python.org/downloads/
2. Click the big yellow **"Download Python 3.12.X"** button (or latest 3.8+)
3. A file named `python-3.12.X-amd64.exe` will download (size ~100MB)

### 2.2 Install Python - IMPORTANT!
1. Double-click the downloaded `.exe` file
2. **IMPORTANT**: Check the box that says **"Add Python 3.X to PATH"** ⚠️
   - This is crucial! Without this, Python won't work from command line
3. Click **"Install Now"**
4. Wait for installation to complete
5. You should see a screen saying "Setup was successful" → Click **"Close"**

### 2.3 Verify Python Installation
1. Open **Command Prompt** or **PowerShell**:
   - Press `Windows Key + R`
   - Type `cmd` and press Enter
   - Or right-click desktop → **"Open PowerShell here"**
2. Type this command and press Enter:
   ```bash
   python --version
   ```
3. You should see: `Python 3.X.X`
   - ✅ If you see version: Python is installed correctly
   - ❌ If error: You may not have checked "Add Python to PATH"
     - Solution: Uninstall Python and reinstall, checking the PATH box

### 2.4 Verify pip (Python Package Manager)
1. In the same Command Prompt/PowerShell, type:
   ```bash
   pip --version
   ```
2. You should see: `pip X.X.X from ...`
   - ✅ If you see version: pip is ready

---

## Step 3: Clone the Repository

### 3.1 Create a Project Folder
1. Open File Explorer
2. Go to a location where you want to store projects (e.g., `C:\Users\YourUsername\Documents`)
3. Right-click in empty space → **"New"** → **"Folder"**
4. Name it `PersonalizedTutorAgent` (or any name you prefer)
5. Open this folder (double-click)
6. Right-click in the folder → **"Open PowerShell here"**

### 3.2 Clone the Repository
1. In PowerShell, copy and paste this command:
   ```bash
   git clone https://github.com/yourusername/PersonalizedTutorAgent.git
   cd PersonalizedTutorAgent
   ```
   *(Replace `yourusername` with actual repo location if different)*
2. Press Enter
3. Wait for download to complete (takes 1-2 minutes)
4. You'll see folder contents appearing

### 3.3 Verify Repository
1. In PowerShell, type:
   ```bash
   dir
   ```
2. You should see:
   - `src/` folder
   - `data/` folder
   - `reports/` folder
   - `app.py` file
   - `run_pipeline.py` file
   - `requirements.txt` file
   - Other files and folders
   - ✅ If you see these: Repository is cloned correctly

---

## Step 4: Create Python Virtual Environment

### 4.1 Why Virtual Environment?
- Keeps project dependencies isolated
- Prevents conflicts with other Python projects
- Best practice for Python development

### 4.2 Create Virtual Environment
1. In PowerShell (in project folder), type:
   ```bash
   python -m venv venv
   ```
2. Press Enter
3. Wait 30 seconds - a `venv` folder will be created

### 4.3 Activate Virtual Environment
1. Type this command:
   ```bash
   .\venv\Scripts\Activate.ps1
   ```
2. Press Enter
3. You should see `(venv)` at the start of your command prompt
   - ✅ If you see `(venv)`: Virtual environment is active
   - ❌ If error about execution policy: Run this first:
     ```bash
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
     Then try activation again

---

## Step 5: Install Python Dependencies

### 5.1 Upgrade pip
1. In PowerShell (with virtual environment active - showing `(venv)`), type:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Press Enter
3. Wait for completion

### 5.2 Install All Requirements
1. In PowerShell, type:
   ```bash
   pip install -r requirements.txt
   ```
2. Press Enter
3. Wait for installation (5-10 minutes depending on internet speed)
4. You'll see downloading messages like:
   ```
   Collecting pandas
   Downloading pandas-2.3.3-cp312-cp312-win_amd64.whl (11.1 MB)
   Collecting numpy
   ...
   Successfully installed pandas numpy scikit-learn streamlit plotly scipy matplotlib seaborn python-dotenv
   ```

### 5.3 Understanding the Packages
The `requirements.txt` file contains:
- **pandas** (2.0.3): Data manipulation and analysis
- **numpy** (1.24.3): Numerical computing
- **scikit-learn** (1.3.0): Machine learning algorithms
- **streamlit** (1.28.0): **Web dashboard framework** ⭐
- **plotly** (5.17.0): Interactive visualizations
- **scipy** (1.11.2): Scientific computing
- **matplotlib** (3.7.2): Static plots and charts
- **seaborn** (0.12.2): Statistical data visualization
- **python-dotenv** (1.0.0): Environment variable management

### 5.4 Verify Installation
1. Type this command:
   ```bash
   pip list
   ```
2. You should see:
   - pandas
   - numpy
   - scikit-learn
   - streamlit ⭐
   - plotly
   - scipy
   - matplotlib
   - seaborn
   - python-dotenv
   
   ✅ If you see all these packages: Installation successful!

### 5.5 Verify Streamlit Specifically
1. Type this command to test Streamlit:
   ```bash
   streamlit --version
   ```
2. You should see: `Streamlit, version X.XX.X`
   - ✅ If you see version: Streamlit is ready
   - ❌ If error: Run `pip install streamlit==1.28.0` again

---

## Step 6: Run the System

### 6.1 Generate Data & Run Pipeline
1. In PowerShell (with virtual environment active), type:
   ```bash
   python run_pipeline.py
   ```
2. Press Enter
3. Wait 2-5 minutes for execution
4. You'll see output like:
   ```
   ╔════════════════════════════════════════════════════════════╗
   ║    PERSONALIZED TUTOR AGENT - COMPLETE PIPELINE            ║
   ╚════════════════════════════════════════════════════════════╝
   
   STEP 1: SYNTHETIC DATA GENERATION
   ✓ Dataset generated successfully!
   ...
   ```
5. When complete, you'll see:
   ```
   ✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!
   ```

---

## Step 7: Launch Interactive Dashboard with Streamlit

### 7.1 What is Streamlit?
Streamlit is a Python framework that turns your code into an interactive web application instantly. No HTML, CSS, or JavaScript needed!

### 7.2 Start Streamlit Dashboard
1. In PowerShell (with virtual environment active), type:
   ```bash
   streamlit run app.py
   ```
2. Press Enter
3. You should see output like:
   ```
   Collecting usage statistics. To deactivate, set browser.gatherUsageStats to False.
   
   You can now view your Streamlit app in your browser.

   Local URL: http://localhost:8501
   Network URL: http://192.168.X.X:8501
   ```

### 7.3 Access the Dashboard
- **Automatically**: A browser window should open automatically at `http://localhost:8501`
- **Manually**: If not, open your browser and go to `http://localhost:8501`

### 7.4 Dashboard Features
Once loaded, you'll see the **Personalized Tutor Agent Dashboard** with:
- **Dashboard Tab**: 📊 View overall metrics and system status
- **Interactive Quiz Tab**: 📝 Take practice quizzes with adaptive difficulty
- **Learning Path Tab**: 🛤️ See your personalized learning sequence
- **Analytics Tab**: 📈 View detailed performance metrics and graphs
- **System Info Tab**: ℹ️ Project information and technical details

### 7.5 Streamlit Navigation
- **Sidebar** (left): Switch between tabs
- **Refresh Button**: Click the circular arrow (top right) to refresh data
- **Menu Button** (≡): Settings and app info

### 7.6 Troubleshooting Streamlit

#### Issue: Browser doesn't open automatically
- **Solution**: Copy the URL from terminal and paste into browser:
  - Example: `http://localhost:8501`

#### Issue: Port 8501 already in use
- **Solution**: Use a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```
- Then access at: `http://localhost:8502`

#### Issue: Dashboard is blank or shows error
- **Solution**:
  1. Make sure `python run_pipeline.py` completed successfully
  2. Close and restart Streamlit:
     ```bash
     Ctrl + C
     streamlit run app.py
     ```
  3. Refresh browser (Ctrl + F5)

#### Issue: Slow or freezing dashboard
- **Solution**:
  1. Close other browser tabs and applications
  2. Check internet connection
  3. Restart Streamlit

### 7.7 Stop the Dashboard
1. In PowerShell, press `Ctrl + C` (hold Ctrl and press C)
2. Type `y` (or just press Enter) and press Enter to confirm
3. Dashboard will shut down

### 7.8 Restart Dashboard
1. Simply type again:
   ```bash
   streamlit run app.py
   ```
2. Dashboard will launch with refreshed data

---

## Step 6: Run the System

### 6.1 Generate Data & Run Pipeline
1. In PowerShell (with virtual environment active), type:
   ```bash
   python run_pipeline.py
   ```
2. Press Enter
3. Wait 2-5 minutes for execution
4. You'll see output like:
   ```
   ╔════════════════════════════════════════════════════════════╗
   ║    PERSONALIZED TUTOR AGENT - COMPLETE PIPELINE            ║
   ╚════════════════════════════════════════════════════════════╝
   
   STEP 1: SYNTHETIC DATA GENERATION
   ✓ Dataset generated successfully!
   ...
   ```
5. When complete, you'll see:
   ```
   ✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!
   ```

### 6.2 Launch Interactive Dashboard
1. In PowerShell, type:
   ```bash
   streamlit run app.py
   ```
2. Press Enter
3. A browser window will open at `http://localhost:8501`
4. You'll see the **Personalized Tutor Agent Dashboard** 🎉

### 6.3 Using the Dashboard
- **Dashboard Tab**: View overall metrics
- **Interactive Quiz Tab**: Take practice quizzes
- **Learning Path Tab**: See personalized learning sequence
- **Analytics Tab**: View detailed performance metrics
- **System Info Tab**: Project information

### 6.4 Stop the Dashboard
1. In PowerShell, press `Ctrl + C` (hold Ctrl and press C)
2. Type `y` and press Enter to confirm

---

# 🍎 MAC INSTALLATION GUIDE

## Step 1: Install Homebrew (Mac Package Manager)

### 1.1 Open Terminal
1. Press `Cmd + Space`
2. Type `terminal` and press Enter

### 1.2 Install Homebrew
1. Copy and paste this command into Terminal:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Press Enter
3. Enter your Mac password when prompted
4. Wait for installation (5-10 minutes)

### 1.3 Verify Homebrew
1. Type:
   ```bash
   brew --version
   ```
2. You should see version number

---

## Step 2: Install Git

1. In Terminal, type:
   ```bash
   brew install git
   ```
2. Press Enter
3. Wait for installation

### Verify Git
1. Type:
   ```bash
   git --version
   ```
2. You should see version number

---

## Step 3: Install Python

1. In Terminal, type:
   ```bash
   brew install python3
   ```
2. Press Enter
3. Wait for installation

### Verify Python
1. Type:
   ```bash
   python3 --version
   ```
2. You should see `Python 3.X.X`

---

## Step 4: Clone Repository

1. Go to desired location in Terminal:
   ```bash
   cd ~/Documents
   ```
2. Clone repository:
   ```bash
   git clone https://github.com/yourusername/PersonalizedTutorAgent.git
   cd PersonalizedTutorAgent
   ```
3. Verify contents:
   ```bash
   ls
   ```

---

## Step 5: Create Virtual Environment

1. In Terminal, type:
   ```bash
   python3 -m venv venv
   ```
2. Press Enter
3. Activate:
   ```bash
   source venv/bin/activate
   ```
4. You should see `(venv)` in prompt

---

## Step 6: Install Dependencies

1. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Wait for completion

---

## Step 7: Run System

1. Run pipeline:
   ```bash
   python run_pipeline.py
   ```
2. Launch dashboard:
   ```bash
   streamlit run app.py
   ```

---

# 🐧 LINUX INSTALLATION GUIDE

## Step 1: Install Git and Python

### For Ubuntu/Debian:
```bash
sudo apt update
sudo apt install git python3 python3-pip python3-venv
```

### For Fedora/RHEL:
```bash
sudo dnf install git python3 python3-pip
```

### Verify:
```bash
git --version
python3 --version
pip3 --version
```

---

## Step 2: Clone Repository

1. Navigate to desired location:
   ```bash
   cd ~/Documents
   ```
2. Clone:
   ```bash
   git clone https://github.com/yourusername/PersonalizedTutorAgent.git
   cd PersonalizedTutorAgent
   ```

---

## Step 3: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 5: Run System

```bash
python3 run_pipeline.py
streamlit run app.py
```

---

# 🔧 Troubleshooting

## Problem: "Python not found" or "Python is not recognized"

### Solution:
1. **Windows**: 
   - Uninstall Python completely
   - Reinstall Python
   - **MAKE SURE** to check "Add Python to PATH"
   - Restart computer
   - Try again

2. **Mac/Linux**:
   - Use `python3` instead of `python`
   - Or create alias: `alias python=python3`

---

## Problem: "pip not found"

### Solution:
```bash
python -m pip install --upgrade pip
```

Then use:
```bash
python -m pip install -r requirements.txt
```

---

## Problem: Virtual Environment Won't Activate (Windows)

### Solution:
1. Open PowerShell as Administrator
2. Run:
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Type `Y` and press Enter
4. Try activating again:
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

---

## Problem: "ModuleNotFoundError: No module named 'pandas'"

### Solution:
1. Make sure virtual environment is active (you see `(venv)` in prompt)
2. Install all requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Wait for complete installation

---

## Problem: Streamlit Dashboard Won't Open

### Solution 1: Check Port Availability
```bash
# Try using a different port
streamlit run app.py --server.port 8502
```
Then access at: `http://localhost:8502`

### Solution 2: Browser Not Opening Automatically
1. Check terminal output for the URL (looks like: `http://localhost:8501`)
2. Copy the URL manually into your web browser
3. The dashboard should load

### Solution 3: Dashboard is Blank or Shows Error
1. Stop Streamlit: Press `Ctrl + C` in terminal
2. Run pipeline first:
   ```bash
   python run_pipeline.py
   ```
3. Then restart Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Refresh browser (Ctrl + F5)

### Solution 4: "ModuleNotFoundError" in Streamlit
- **Cause**: Streamlit app can't find your Python modules
- **Solution**:
  1. Make sure you're in the project root directory
  2. Verify virtual environment is active (shows `(venv)` in prompt)
  3. Reinstall streamlit:
     ```bash
     pip install --upgrade streamlit==1.28.0
     ```
  4. Restart dashboard

### Solution 5: Streamlit is Slow or Freezing
- **Cause**: Too many running applications or network issues
- **Solution**:
  1. Close other browser tabs and applications
  2. Restart Streamlit:
     ```bash
     Ctrl + C
     streamlit run app.py
     ```
  3. Check internet connection

### Solution 6: "Streamlit not found" Error
- **Cause**: Streamlit not installed or virtual environment not active
- **Solution**:
  1. Activate virtual environment:
     ```bash
     .\venv\Scripts\Activate.ps1  # Windows
     source venv/bin/activate      # Mac/Linux
     ```
  2. Install Streamlit:
     ```bash
     pip install streamlit==1.28.0
     ```
  3. Try running app again:
     ```bash
     streamlit run app.py
     ```

---

## Problem: Streamlit Dashboard Won't Open

### Solution:
1. Make sure no other application is using port 8501
2. Try this command:
   ```bash
   streamlit run app.py --server.port 8502
   ```
3. Browser will open at `http://localhost:8502`

---

## Problem: Unicode/Encoding Errors on Windows

### Solution:
This is fixed in the latest version. If you see it:
1. Make sure you're using Python 3.8+
2. Update the code (included in this version)
3. Try again

---

## Problem: Installation Takes Forever

### Causes:
- Slow internet connection
- Computer is busy with other tasks

### Solution:
1. Try on a faster internet connection
2. Close other applications
3. Try reinstalling:
   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```

---

# ✅ Verification Checklist

After installation, verify everything works:

### 1. Check All Files
```bash
# You should see these files/folders:
dir          # Windows
ls           # Mac/Linux
```

Look for:
- [ ] `src/` folder
- [ ] `data/` folder
- [ ] `reports/` folder
- [ ] `app.py` file
- [ ] `run_pipeline.py` file
- [ ] `requirements.txt` file
- [ ] `venv/` folder (virtual environment)

### 2. Check Python
```bash
python --version  # Should be 3.8 or higher
```
- [ ] Python version 3.8+

### 3. Check pip
```bash
pip list
```

You should see:
- [ ] pandas
- [ ] numpy
- [ ] scikit-learn
- [ ] streamlit
- [ ] plotly
- [ ] scipy
- [ ] matplotlib
- [ ] seaborn
- [ ] python-dotenv

### 4. Check Virtual Environment
```bash
# You should see (venv) at start of your prompt
```
- [ ] `(venv)` shown in command prompt

### 5. Test Pipeline
```bash
python run_pipeline.py
```

Look for:
- [ ] "Dataset generated successfully!"
- [ ] "DKT model initialized!"
- [ ] "PIPELINE EXECUTION COMPLETED SUCCESSFULLY!"

### 6. Test Dashboard
```bash
streamlit run app.py
```

- [ ] Browser opens automatically
- [ ] Dashboard displays with 5 tabs
- [ ] No error messages

---

# 🎯 First-Time User Walkthrough

Once everything is installed:

## 1. Generate Initial Data
```bash
python run_pipeline.py
```
This creates:
- Student profiles
- Learning data
- Evaluation reports

## 2. Launch Dashboard
```bash
streamlit run app.py
```

## 3. Explore Features
- **Dashboard**: View system overview
- **Quiz**: Take interactive quiz
- **Learning Path**: See personalized path
- **Analytics**: View detailed metrics

## 4. Read Documentation
- Open `README.md` for detailed info
- Check `QUICK_REFERENCE.md` for examples
- Review `reports/research_report_generator.py` for technical details

---

# 🆘 Getting Help

### Common Issues:
1. **Installation help**: See [Troubleshooting](#troubleshooting) section above
2. **Using the system**: Check `README.md`
3. **Code examples**: See `QUICK_REFERENCE.md`
4. **System design**: Read `reports/architecture.py`

### Before Asking for Help:
- [ ] You have Python 3.8+
- [ ] Virtual environment is active
- [ ] All files in `requirements.txt` are installed
- [ ] You've run `python run_pipeline.py` successfully

---

# 📞 Quick Reference Commands

| Task | Command |
|------|---------|
| **Clone repository** | `git clone <repo-url>` |
| **Create virtual env** | `python -m venv venv` |
| **Activate virtual env (Win)** | `.\venv\Scripts\Activate.ps1` |
| **Activate virtual env (Mac/Linux)** | `source venv/bin/activate` |
| **Deactivate virtual env** | `deactivate` |
| **Install dependencies** | `pip install -r requirements.txt` |
| **Run pipeline** | `python run_pipeline.py` |
| **Launch dashboard** | `streamlit run app.py` |
| **Check installed packages** | `pip list` |
| **Check Python version** | `python --version` |

---

# 🎓 What Happens When You Run the System?

## Step-by-Step Execution

### 1. Run `python run_pipeline.py`
   - Generates synthetic student data
   - Creates 50 student profiles
   - Generates 3,000 learning interactions
   - Creates 80 quiz questions

### 2. Learner Profiling
   - Analyzes each student's performance
   - Calculates mastery probability
   - Identifies strengths and weaknesses

### 3. Knowledge Tracing
   - Trains simplified Deep Knowledge Tracing (DKT) model
   - Predicts student knowledge evolution
   - Achieves ~60% prediction accuracy

### 4. Learning Path Generation
   - Creates personalized learning sequences
   - Orders concepts by difficulty
   - Respects prerequisite constraints

### 5. Adaptive Quiz
   - Generates dynamic quiz questions
   - Adjusts difficulty based on performance
   - Maintains 65% target accuracy (Zone of Proximal Development)

### 6. Tutor Agent
   - Generates personalized feedback
   - Provides multi-level hints
   - Offers motivational messages

### 7. Evaluation
   - Calculates learning metrics
   - Generates performance report
   - Creates learning curves visualization

### Output Files
```
data/
  ├── student_interactions.csv  (3,000 records)
  └── question_bank.csv         (80 questions)

reports/
  ├── evaluation_report.txt     (comprehensive metrics)
  └── learning_curves.png       (performance visualization)
```

---

# 🚀 You're Ready!

Once you complete all steps:
1. ✅ You have Python 3.8+
2. ✅ You have Git installed
3. ✅ You cloned the repository
4. ✅ You created virtual environment
5. ✅ You installed dependencies
6. ✅ You can run the pipeline
7. ✅ You can launch the dashboard

**Congratulations! The system is ready to use! 🎉**

---

## Next Steps:
1. Read [README.md](README.md) for detailed documentation
2. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for code examples
3. Explore [INDEX.md](INDEX.md) for complete file guide
4. Review [COMPLETION_REPORT.md](COMPLETION_REPORT.md) for project status

---

**Happy Learning! 🎓**
