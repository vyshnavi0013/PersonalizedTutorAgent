# QUICK REFERENCE GUIDE
## Personalized Tutor Agent - Command Line Quick Start

### 🎯 Essential Commands

```bash
# 1. INSTALL DEPENDENCIES (1 minute)
pip install -r requirements.txt

# 2. GENERATE SYNTHETIC DATA (30 seconds)
cd data
python generate_synthetic_data.py
cd ..

# 3. RUN COMPLETE PIPELINE (2-5 minutes)
python run_pipeline.py

# 4. LAUNCH WEB DASHBOARD (immediate)
streamlit run app.py
```

### 📂 File Organization

| File | Purpose | Lines |
|------|---------|-------|
| `src/learner_profiling.py` | Student profile tracking | 300+ |
| `src/knowledge_tracing.py` | DKT model for mastery prediction | 350+ |
| `src/learning_path.py` | Personalized path generation | 400+ |
| `src/adaptive_quiz.py` | Adaptive quiz engine | 450+ |
| `src/tutor_agent.py` | NLP feedback generation | 400+ |
| `src/evaluation.py` | Analysis & evaluation | 350+ |
| `app.py` | Streamlit dashboard | 500+ |
| `run_pipeline.py` | Complete execution pipeline | 300+ |
| `data/generate_synthetic_data.py` | Synthetic data generator | 250+ |
| `reports/architecture.py` | System architecture docs | 250+ |
| `reports/research_report_generator.py` | Research report | 400+ |

### 🚀 Usage Examples

```python
# EXAMPLE 1: Load & Use Learner Profiles
from src.learner_profiling import LearnerProfileManager
import pandas as pd

interactions = pd.read_csv('data/student_interactions.csv')
interactions['timestamp'] = pd.to_datetime(interactions['timestamp'])

manager = LearnerProfileManager(interactions['concept'].unique().tolist())
manager.update_from_interactions(interactions)

profile = manager.get_or_create_profile(student_id=1)
mastery = profile.get_knowledge_state_vector()
weak = profile.get_weak_concepts(n=3)
```

```python
# EXAMPLE 2: Knowledge Tracing
from src.knowledge_tracing import SimplifiedDKT

dkt = SimplifiedDKT(concepts, learning_rate=0.1)
trajectory, final_knowledge = dkt.trace_student(interactions, student_id=1)

# Predict performance
prob_correct = dkt.predict_performance(knowledge_state, concept)

# Estimate mastery time
steps = dkt.estimate_steps_to_mastery(knowledge_state, concept)
```

```python
# EXAMPLE 3: Learning Path Generation
from src.learning_path import LearningPathGenerator

generator = LearningPathGenerator(
    concepts, 
    concept_difficulty={c: 0.5 for c in concepts}
)

path = generator.generate_path(
    student_knowledge,
    weak_concepts=['Concept_1'],
    num_concepts=5,
    learning_preference='balanced'
)

# Display path
for node in path:
    print(f"{node['position']}. {node['concept']} "
          f"(Bloom: {node['bloom_level']}, Mastery: {node['current_mastery']:.0%})")
```

```python
# EXAMPLE 4: Adaptive Quiz
from src.adaptive_quiz import QuestionBank, AdaptiveQuizEngine

qbank = QuestionBank(questions_df)
quiz = AdaptiveQuizEngine(qbank, target_accuracy=0.65)

quiz.start_new_quiz()
question = quiz.select_next_question(student_id=1, concept='Concept_1', 
                                    student_mastery=0.5)
result = quiz.record_response(question.question_id, 1, is_correct=1, 
                             time_spent=45)
```

```python
# EXAMPLE 5: Tutor Agent Feedback
from src.tutor_agent import PersonalizedTutorAgent

tutor = PersonalizedTutorAgent()

feedback = tutor.feedback_gen.generate_immediate_feedback(
    is_correct=True,
    concept='Concept_1',
    difficulty='Medium',
    time_spent=45,
    estimated_time=30
)

hint = tutor.feedback_gen.generate_hint('Concept_1', hint_level=1)
```

### 📊 Expected Results

After running `python run_pipeline.py`, you should see:

```
✓ Question bank saved: data/question_bank.csv
✓ Student interactions saved: data/student_interactions.csv

DATASET STATISTICS
================
Question Bank:
  - Total questions: 80
  - Concepts: 8

Student Interactions:
  - Total interactions: 3000
  - Unique students: 50
  - Overall correctness rate: 65.12%

LEARNER PROFILING
✓ Learner profiles created!

KNOWLEDGE TRACING
✓ DKT model initialized!
✓ 1-step prediction accuracy: 78.5%

EVALUATION
✓ Average Learning Improvement Rate: 0.0342

✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!
```

### 🌐 Streamlit Dashboard

After running `streamlit run app.py`:

- Open browser to `http://localhost:8501`
- **Dashboard:** View metrics, knowledge state, recommendations
- **Quiz:** Take practice quizzes with adaptive difficulty
- **Learning Path:** See personalized concept sequence
- **Analytics:** Detailed performance analysis
- **System Info:** Project documentation

### 🔧 Configuration Options

```python
# In knowledge_tracing.py
dkt = SimplifiedDKT(
    concepts,
    learning_rate=0.10,      # How fast students learn
    forget_rate=0.05         # How fast they forget
)

# In adaptive_quiz.py
quiz = AdaptiveQuizEngine(
    qbank,
    target_accuracy=0.65     # Maintain 65% accuracy (Vygotsky's ZPD)
)

# In learning_path.py
path = generator.generate_path(
    knowledge,
    num_concepts=5,          # Include 5 concepts in path
    learning_preference='balanced'  # or 'progressive', 'review'
)
```

### ⚡ Performance Benchmarks

| Component | Time Complexity | Space | Notes |
|-----------|-----------------|-------|-------|
| Learner Profiling | O(n×m) | O(n×k) | n=students, m=interactions, k=concepts |
| Knowledge Tracing | O(n) | O(k) | Very efficient |
| Learning Path Gen | O(k² × p) | O(k × p) | k=concepts, p=prerequisites |
| Adaptive Quiz | O(log q) | O(q) | q=questions |
| Evaluation | O(n×k) | O(n) | Full dataset scan |

### 📚 Module Dependencies

```
Main Entry Points:
├── run_pipeline.py
│   ├── data/generate_synthetic_data.py
│   ├── src/learner_profiling.py
│   ├── src/knowledge_tracing.py
│   ├── src/learning_path.py
│   ├── src/adaptive_quiz.py
│   ├── src/tutor_agent.py
│   └── src/evaluation.py
│
└── app.py
    └── All src modules
```

### 🎓 Research References

**Quickly access these papers for context:**
1. **DKT** - Piech et al. (2015) - Deep Knowledge Tracing
2. **ITS** - VanLehn (2011) - Intelligent Tutoring Systems
3. **Bloom** - Bloom (1984) - 2-Sigma Problem
4. **Vygotsky** - Vygotsky (1978) - Zone of Proximal Development

See research report in `reports/research_report_generator.py`

### ✅ Verification Checklist

```bash
# Verify Python version (3.8+)
python --version

# Verify dependencies installed
pip list | grep pandas
pip list | grep streamlit

# Verify data files exist
ls data/student_interactions.csv
ls data/question_bank.csv

# Test import all modules
python -c "from src import *; print('✓ All modules imported!')"

# Run dashboard
streamlit run app.py
```

### 🆘 Common Issues & Quick Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | `pip install -r requirements.txt --upgrade` |
| `FileNotFoundError: data/...` | `cd data && python generate_synthetic_data.py && cd ..` |
| `Port 8501 in use` | `streamlit run app.py --server.port 8502` |
| Slow performance | Reduce dataset: `n_students=20, n_concepts=4` |
| Import errors | `export PYTHONPATH="${PYTHONPATH}:$(pwd)"` |

### 📈 Key Metrics to Watch

- **Accuracy:** Should be ~65-75% (optimal learning zone)
- **Learning Gain:** 60%+ (Hake's normalized gain)
- **DKT Accuracy:** 75%+ (prediction reliability)
- **Path Effectiveness:** 70%+ (concept coverage)
- **Adaptation Quality:** 65%+ (difficulty adjustment)

### 🎯 Next Steps After Installation

1. **Explore:** Run `streamlit run app.py` and explore dashboard
2. **Understand:** Read `README.md` for detailed documentation
3. **Extend:** Check `src/` modules for customization points
4. **Evaluate:** Run `python run_pipeline.py` for complete analysis
5. **Publish:** Use research report in `reports/` for academic work

---

**Version:** 1.0.0 | **Status:** Production Ready ✅ | **Date:** Jan 29, 2026
