"""
Setup Instructions and Quick Start Guide
Personalized Tutor Agent
"""

SETUP_GUIDE = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        SETUP & INSTALLATION GUIDE                           ║
║              Personalized Tutor Agent - Learning Path Generator              ║
╚══════════════════════════════════════════════════════════════════════════════╝


📋 SYSTEM REQUIREMENTS
══════════════════════════════════════════════════════════════════════════════

• Python 3.8 or higher
• pip (Python package manager)
• 500 MB free disk space
• Modern web browser (for Streamlit dashboard)
• Windows / macOS / Linux


🚀 QUICK START (5 MINUTES)
══════════════════════════════════════════════════════════════════════════════

1. NAVIGATE TO PROJECT DIRECTORY
   ───────────────────────────────────────────────────────────────────────────
   
   cd /path/to/PersonalizedTutorAgent


2. CREATE VIRTUAL ENVIRONMENT (Recommended)
   ───────────────────────────────────────────────────────────────────────────
   
   Windows:
   $ python -m venv venv
   $ venv\\Scripts\\activate
   
   macOS/Linux:
   $ python3 -m venv venv
   $ source venv/bin/activate


3. INSTALL DEPENDENCIES
   ───────────────────────────────────────────────────────────────────────────
   
   $ pip install -r requirements.txt
   
   This installs:
   • pandas (data manipulation)
   • numpy (numerical computing)
   • scikit-learn (ML utilities)
   • streamlit (web interface)
   • plotly (interactive visualizations)
   • scipy (statistical analysis)
   • matplotlib & seaborn (plotting)


4. GENERATE SYNTHETIC DATA
   ───────────────────────────────────────────────────────────────────────────
   
   $ cd data
   $ python generate_synthetic_data.py
   $ cd ..
   
   This creates:
   • student_interactions.csv (3,000 records)
   • question_bank.csv (80 questions)
   
   Output:
   ✓ Question bank saved: data/question_bank.csv
   ✓ Student interactions saved: data/student_interactions.csv


5. RUN COMPLETE PIPELINE (Optional but Recommended)
   ───────────────────────────────────────────────────────────────────────────
   
   $ python run_pipeline.py
   
   This executes the complete system:
   ✓ Data generation & statistics
   ✓ Learner profiling (50 students)
   ✓ Knowledge tracing initialization
   ✓ Learning path generation (sample)
   ✓ Adaptive quiz setup
   ✓ Tutor agent initialization
   ✓ Comprehensive evaluation
   ✓ Report generation
   
   Duration: ~2-5 minutes
   Outputs: Reports in /reports directory


6. LAUNCH STREAMLIT DASHBOARD
   ───────────────────────────────────────────────────────────────────────────
   
   $ streamlit run app.py
   
   Output should show:
   
   You can now view your Streamlit app in your browser.
   
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   
   Browser automatically opens dashboard.


✅ VERIFY INSTALLATION
══════════════════════════════════════════════════════════════════════════════

Check all components working:

$ python -c "
from src.learner_profiling import LearnerProfileManager
from src.knowledge_tracing import SimplifiedDKT
from src.learning_path import LearningPathGenerator
from src.adaptive_quiz import QuestionBank
from src.tutor_agent import PersonalizedTutorAgent
print('✓ All modules imported successfully!')
"

Expected output:
✓ All modules imported successfully!


📂 PROJECT STRUCTURE OVERVIEW
══════════════════════════════════════════════════════════════════════════════

PersonalizedTutorAgent/
│
├── src/                              # Core implementation modules
│   ├── learner_profiling.py         # Student profile tracking
│   ├── knowledge_tracing.py         # DKT model
│   ├── learning_path.py             # Path generation
│   ├── adaptive_quiz.py             # Quiz engine
│   ├── tutor_agent.py               # NLP feedback
│   └── evaluation.py                # Analysis framework
│
├── data/                             # Data layer
│   ├── generate_synthetic_data.py   # Data generator
│   ├── student_interactions.csv     # Generated (run generator first)
│   └── question_bank.csv            # Generated (run generator first)
│
├── reports/                          # Documentation & results
│   ├── research_report_generator.py
│   ├── architecture.py
│   ├── evaluation_report.txt        # Generated after pipeline run
│   └── learning_curves.png          # Generated visualization
│
├── app.py                            # Streamlit application
├── run_pipeline.py                   # Complete execution pipeline
├── requirements.txt                  # Dependencies
├── README.md                         # Full documentation
└── SETUP_INSTRUCTIONS.md             # This file


🎯 COMMON USE CASES
══════════════════════════════════════════════════════════════════════════════

USE CASE 1: Just Generate Data
────────────────────────────────────────────────────────────────────────────
$ cd data
$ python generate_synthetic_data.py
$ cd ..

Files created:
✓ data/student_interactions.csv
✓ data/question_bank.csv

Time: ~30 seconds


USE CASE 2: Run Evaluation Pipeline
────────────────────────────────────────────────────────────────────────────
$ python run_pipeline.py

Complete evaluation with:
✓ Data generation
✓ Learner profiling
✓ Knowledge tracing
✓ Learning paths
✓ Quiz engine
✓ Tutor agent
✓ Analysis & reports

Time: 2-5 minutes
Output: reports/evaluation_report.txt


USE CASE 3: Interactive Dashboard Only
────────────────────────────────────────────────────────────────────────────
# Generate data first
$ cd data && python generate_synthetic_data.py && cd ..

# Launch dashboard
$ streamlit run app.py

Access at: http://localhost:8501


USE CASE 4: Run Specific Module
────────────────────────────────────────────────────────────────────────────
$ python -c "
from src.learner_profiling import LearnerProfileManager
import pandas as pd

# Load data
interactions = pd.read_csv('data/student_interactions.csv')
interactions['timestamp'] = pd.to_datetime(interactions['timestamp'])

# Create profiles
manager = LearnerProfileManager(
    interactions['concept'].unique().tolist()
)
manager.update_from_interactions(interactions)

# Get summary
print(manager.get_learner_profiles_summary())
"


🔧 CONFIGURATION OPTIONS
══════════════════════════════════════════════════════════════════════════════

MODIFY DATASET GENERATION:
─────────────────────────────────────────────────────────────────────────────

In data/generate_synthetic_data.py:

    generator = SyntheticDatasetGenerator(
        n_students=100,        # Change number of students
        n_concepts=12,         # Change number of concepts
        n_questions=150,       # Change question bank size
        seed=42                # Set seed for reproducibility
    )


MODIFY DKT PARAMETERS:
─────────────────────────────────────────────────────────────────────────────

In src/knowledge_tracing.py:

    dkt = SimplifiedDKT(
        concepts=concepts,
        learning_rate=0.15,    # Higher = faster learning
        forget_rate=0.08       # Higher = faster forgetting
    )


MODIFY LEARNING PATH GENERATION:
─────────────────────────────────────────────────────────────────────────────

In src/learning_path.py:

    path = generator.generate_path(
        student_knowledge,
        num_concepts=8,        # Number of concepts in path
        max_difficulty=0.9,    # Maximum difficulty to include
        learning_preference='progressive'  # or 'balanced', 'review'
    )


⚠️ TROUBLESHOOTING
══════════════════════════════════════════════════════════════════════════════

ISSUE 1: "ModuleNotFoundError: No module named 'streamlit'"
─────────────────────────────────────────────────────────────────────────────
Solution:
$ pip install streamlit==1.28.0

Or reinstall all:
$ pip install -r requirements.txt --upgrade


ISSUE 2: "FileNotFoundError: data/student_interactions.csv"
─────────────────────────────────────────────────────────────────────────────
Solution:
Generate the data first:
$ cd data
$ python generate_synthetic_data.py
$ cd ..


ISSUE 3: "ImportError: cannot import name 'LearnerProfile' from 'src'"
─────────────────────────────────────────────────────────────────────────────
Solution:
Ensure PYTHONPATH includes src:
$ export PYTHONPATH="${PYTHONPATH}:$(pwd)"

Or add to Python script:
import sys
sys.path.insert(0, './src')


ISSUE 4: Streamlit App Runs But Dashboard Is Empty
─────────────────────────────────────────────────────────────────────────────
Solution:
1. Check data files exist:
   $ ls -la data/student_interactions.csv
   $ ls -la data/question_bank.csv

2. Check data not corrupted:
   $ python -c "import pandas as pd; print(len(pd.read_csv('data/student_interactions.csv')))"

3. Restart app:
   Press Ctrl+C and run again:
   $ streamlit run app.py


ISSUE 5: Slow Performance / Memory Issues
─────────────────────────────────────────────────────────────────────────────
Solution:
Reduce dataset size in generate_synthetic_data.py:

    generator = SyntheticDatasetGenerator(
        n_students=20,      # Reduce from 50
        n_concepts=4,       # Reduce from 8
        n_questions=40      # Reduce from 80
    )


ISSUE 6: "pandas.errors.ParserError" when loading CSV
─────────────────────────────────────────────────────────────────────────────
Solution:
Regenerate the data:
$ cd data
$ rm -f *.csv
$ python generate_synthetic_data.py
$ cd ..


📊 EXPECTED OUTPUT
══════════════════════════════════════════════════════════════════════════════

DATA GENERATION OUTPUT:
───────────────────────────────────────────────────────────────────────────────

✓ Question bank saved: data/question_bank.csv
✓ Student interactions saved: data/student_interactions.csv
  - 3000 total interactions
  - 50 unique students
  - 8 unique concepts

============================================================
DATASET STATISTICS
============================================================

Question Bank:
  - Total questions: 80
  - Concepts: 8
  - Difficulty distribution:
    Easy      27
    Medium    27
    Hard      26


PIPELINE EXECUTION OUTPUT:
───────────────────────────────────────────────────────────────────────────────

════════════════════════════════════════════════════════════
STEP 1: SYNTHETIC DATA GENERATION
════════════════════════════════════════════════════════════
...
✓ Overall Accuracy: 65.12%
✓ Average Time Spent: 49.5 seconds

════════════════════════════════════════════════════════════
STEP 2: LEARNER PROFILING
════════════════════════════════════════════════════════════
...
✓ Learner profiles created!

════════════════════════════════════════════════════════════
...continuing through all steps...

✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!
════════════════════════════════════════════════════════════


STREAMLIT DASHBOARD OUTPUT:
───────────────────────────────────────────────────────────────────────────────

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.105:8501

[Browser opens with dashboard showing]:
- 📊 Dashboard tab with metrics
- 📝 Interactive Quiz tab
- 🛤️ Learning Path tab
- 📈 Analytics tab
- ℹ️ System Info tab


📚 NEXT STEPS
══════════════════════════════════════════════════════════════════════════════

After successful installation:

1. EXPLORE THE DASHBOARD
   ├─ View student profiles
   ├─ Take practice quizzes
   ├─ See learning paths
   └─ Check analytics

2. READ THE DOCUMENTATION
   ├─ README.md (full guide)
   ├─ research_report_generator.py (research report)
   └─ architecture.py (system design)

3. CUSTOMIZE THE SYSTEM
   ├─ Modify dataset parameters
   ├─ Adjust DKT settings
   ├─ Update learning paths
   └─ Extend modules

4. RUN EXPERIMENTS
   ├─ Test different students
   ├─ Evaluate learning gains
   ├─ Compare approaches
   └─ Generate reports

5. EXTEND THE PROJECT
   ├─ Add LSTM-based DKT
   ├─ Implement reinforcement learning
   ├─ Integrate real question banks
   └─ Deploy to production


📞 GETTING HELP
══════════════════════════════════════════════════════════════════════════════

1. Check README.md for detailed documentation
2. Review module docstrings for API details
3. See example usage in each module's __main__ section
4. Check troubleshooting section above
5. Review generated reports (reports/evaluation_report.txt)


🎓 LEARNING RESOURCES
══════════════════════════════════════════════════════════════════════════════

Research Papers Referenced:
• Deep Knowledge Tracing (Piech et al., 2015)
• Intelligent Tutoring Systems (VanLehn, 2011)
• Bloom's 2-Sigma Problem (Bloom, 1984)

Related Datasets:
• EdNet: https://github.com/riiid/ednet
• UCI Student Performance: https://archive.ics.uci.edu/ml


═════════════════════════════════════════════════════════════════════════════

Installation Status Checklist:
☐ Python 3.8+ installed
☐ Virtual environment created
☐ Dependencies installed (pip install -r requirements.txt)
☐ Data generated (python data/generate_synthetic_data.py)
☐ Pipeline executed successfully (python run_pipeline.py)
☐ Streamlit app launched (streamlit run app.py)
☐ Dashboard accessible at http://localhost:8501
☐ All modules imported without errors

Ready to use! 🚀

═════════════════════════════════════════════════════════════════════════════

Version: 1.0.0
Last Updated: January 2026
Status: Production Ready ✅
"""

if __name__ == '__main__':
    print(SETUP_GUIDE)
    
    # Save to file
    with open('SETUP_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write(SETUP_GUIDE)
    print("\n✓ Setup guide saved to: SETUP_INSTRUCTIONS.md")
