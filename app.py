"""
Streamlit Application for Personalized Tutor Agent
Interactive web interface for the tutor system
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from learner_profiling import LearnerProfileManager
from knowledge_tracing import SimplifiedDKT
from learning_path import LearningPathGenerator, AdaptivePathManager
from adaptive_quiz import AdaptiveQuizEngine, QuestionBank, DifficultyAdaptor
from tutor_agent import PersonalizedTutorAgent

# Configure page
st.set_page_config(
    page_title="Personalized Tutor Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-card {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #28a745;
    }
    .warning-card {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #ffc107;
    }
    </style>
""", unsafe_allow_html=True)


class TutorSessionManager:
    """Manages tutor sessions in Streamlit"""
    
    def __init__(self):
        """Initialize session manager"""
        if 'initialized' not in st.session_state:
            self._initialize_session()
    
    def _initialize_session(self):
        """Initialize session state"""
        st.session_state.initialized = True
        st.session_state.logged_in = False
        st.session_state.student_email = None
        st.session_state.student_name = None
        st.session_state.student_id = 1
        st.session_state.selected_subject = None
        st.session_state.student_level = None  # beginner, intermediate, advanced
        st.session_state.assessment_complete = False
        st.session_state.quiz_started = False
        st.session_state.quiz_responses = []
        st.session_state.learning_path = []
        st.session_state.knowledge_state = {}
        st.session_state.interaction_data = None
        st.session_state.current_question_idx = 0
        st.session_state.assessment_responses = []
        st.session_state.current_question_data = None


def create_mock_data():
    """Create mock data for development/testing"""
    # Mock student interactions
    interactions_data = {
        'student_id': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
        'concept_id': ['algebra', 'algebra', 'geometry', 'algebra', 'calculus', 'geometry', 
                       'algebra', 'statistics', 'calculus', 'geometry', 'calculus', 'statistics',
                       'algebra', 'geometry', 'statistics'],
        'question_id': [1, 2, 5, 3, 8, 6, 2, 10, 9, 5, 8, 10, 1, 6, 10],
        'correct': [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
        'time_spent': [45, 32, 58, 40, 90, 35, 38, 42, 65, 55, 48, 39, 30, 40, 70],
        'timestamp': pd.date_range(start='2024-01-01', periods=15, freq='D')
    }
    interactions_df = pd.DataFrame(interactions_data)
    
    # Mock question bank
    qbank_data = {
        'question_id': range(1, 11),
        'concept': ['algebra', 'algebra', 'algebra', 'algebra', 'geometry',
                   'geometry', 'geometry', 'calculus', 'calculus', 'statistics'],
        'difficulty': [1, 2, 2, 3, 1, 2, 3, 2, 3, 2],
        'question_text': [
            'Solve: 2x + 5 = 13',
            'Expand: (x + 2)(x - 3)',
            'Solve: 3x² = 12',
            'Factor: x² + 5x + 6',
            'Find area of triangle with base 5, height 8',
            'Calculate perimeter of rectangle 4×6',
            'Find volume of sphere with radius 3',
            'Find derivative of x³ + 2x²',
            'Integrate: ∫(2x + 1)dx',
            'Calculate mean of: 2, 4, 6, 8, 10'
        ]
    }
    qbank_df = pd.DataFrame(qbank_data)
    
    return interactions_df, qbank_df


def load_data():
    """Load datasets with fallback to mock data"""
    try:
        interactions_df = pd.read_csv('data/student_interactions.csv')
        qbank_df = pd.read_csv('data/question_bank.csv')
        
        # Parse timestamp if exists
        if 'timestamp' in interactions_df.columns:
            interactions_df['timestamp'] = pd.to_datetime(interactions_df['timestamp'])
        
        return interactions_df, qbank_df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.warning("⚠️ Using mock data for demonstration. Real data files not found.")
        return create_mock_data()


def render_login_page():
    """Render login/registration page"""
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 50px auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🎓 Personalized Tutor")
        st.subheader("Welcome to AI-Powered Learning")
        st.markdown("---")
        
        # Login form
        st.subheader("Sign In / Register")
        
        email = st.text_input(
            "Email Address",
            placeholder="student@example.com",
            key="login_email"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        
        name = st.text_input(
            "Full Name (for new users)",
            placeholder="John Doe",
            key="login_name"
        )
        
        if st.button("📝 Sign In / Register", use_container_width=True, type="primary"):
            if email and password:
                st.session_state.logged_in = True
                st.session_state.student_email = email
                st.session_state.student_name = name if name else email.split('@')[0]
                st.session_state.student_id = hash(email) % 1000  # Generate ID from email
                st.success(f"✅ Welcome, {st.session_state.student_name}!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Please enter both email and password")


def render_subject_selection():
    """Render subject selection page"""
    st.title("🎯 Choose Your Learning Subject")
    st.subheader(f"Welcome, {st.session_state.student_name}! 👋")
    
    st.markdown("""
    Select a subject below and we'll analyze your current knowledge level to create a personalized learning path.
    """)
    
    st.markdown("---")
    
    # Subject selection
    subjects = ["Mathematics", "Science", "Biology", "Physics", "Chemistry", "History", "Geography"]
    
    cols = st.columns(3)
    selected_subject = None
    
    for idx, subject in enumerate(subjects):
        col = cols[idx % 3]
        with col:
            if st.button(f"📚 {subject}", use_container_width=True, key=f"subject_{subject}"):
                selected_subject = subject
                st.session_state.selected_subject = subject
                st.rerun()
    
    st.markdown("---")
    st.info("💡 Tip: Choose a subject you'd like to learn or improve at!")


def render_initial_assessment(tutor_agent, qbank, profile_manager, student_id):
    """Render initial assessment to determine student level"""
    st.title(f"📋 Initial Assessment - {st.session_state.selected_subject}")
    st.subheader("Let's analyze your knowledge level...")
    
    # Difficulty progression for assessment
    assessment_difficulties = ["Easy", "Medium", "Hard"]
    
    st.markdown(f"Answer **3 quick questions** to determine your level...")
    st.progress(len(st.session_state.assessment_responses) / 3)
    
    st.write(f"📊 Progress: {len(st.session_state.assessment_responses)}/3 completed")
    
    if len(st.session_state.assessment_responses) < 3:
        current_idx = len(st.session_state.assessment_responses)
        difficulty = assessment_difficulties[current_idx]
        
        # Generate AI question
        st.write("🤖 Generating AI question...")
        try:
            question_data = tutor_agent.generate_quiz_question(
                concept=st.session_state.selected_subject,
                difficulty=difficulty,
                mastery_level=0.5
            )
            
            st.markdown("---")
            
            # Display question prominently
            st.markdown(f"### 📋 Question {current_idx + 1}")
            st.warning(f"**{question_data['question']}**")
            st.info(f"**Difficulty:** {difficulty}")
            
            st.markdown("---")
            
            # Answer selection using a form to prevent auto-submission
            st.markdown("### Select Your Answer")
            with st.form(key=f"assessment_form_{current_idx}", clear_on_submit=False):
                answer = st.radio(
                    "Choose the best answer:",
                    question_data['options'],
                    key=f"assessment_answer_{current_idx}"
                )
                
                # Buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    submit_button = st.form_submit_button("✓ Submit Answer", use_container_width=True, type="primary")
                
                with col2:
                    hint_button = st.form_submit_button("ℹ️ Show Hint", use_container_width=True)
                
                if submit_button:
                    # Check if answer is correct
                    is_correct = (answer == question_data['correct_answer'])
                    
                    st.session_state.assessment_responses.append({
                        'question_id': f'assess_{current_idx + 1}',
                        'difficulty': difficulty,
                        'correct': is_correct,
                        'question': question_data['question'],
                        'student_answer': answer,
                        'correct_answer': question_data['correct_answer'],
                        'explanation': question_data['explanation']
                    })
                    st.rerun()
                
                if hint_button:
                    st.info(f"💡 **Hint:** Consider the key aspects of {st.session_state.selected_subject} and how they apply in practice.")
            
            st.markdown("---")
        
        except Exception as e:
            st.error(f"❌ Error generating question: {e}")
            st.write("Using fallback question...")
            
            # Fallback question
            fallback_question = {
                "question": f"What is a key aspect of {st.session_state.selected_subject}?",
                "options": ["Implementation", "Theory", "Practice", "Examples"],
                "correct_answer": "Practice",
                "explanation": "Practice is essential for mastering any concept."
            }
            
            st.markdown("---")
            st.markdown(f"### 📋 Question {current_idx + 1}")
            st.warning(f"**{fallback_question['question']}**")
            st.info(f"**Difficulty:** {difficulty}")
            
            st.markdown("---")
            
            answer = st.radio(
                "Choose the best answer:",
                fallback_question['options'],
                key=f"assessment_answer_{current_idx}"
            )
            
            # Answer submission using form
            with st.form(key=f"fallback_assessment_form_{current_idx}", clear_on_submit=False):
                col1, col2 = st.columns(2)
                with col1:
                    submit_button = st.form_submit_button("✓ Submit Answer", use_container_width=True, type="primary")
                
                with col2:
                    hint_button = st.form_submit_button("ℹ️ Show Hint", use_container_width=True)
                
                if submit_button:
                    is_correct = (answer == fallback_question['correct_answer'])
                    st.session_state.assessment_responses.append({
                        'question_id': f'assess_{current_idx + 1}',
                        'difficulty': difficulty,
                        'correct': is_correct,
                        'question': fallback_question['question'],
                        'student_answer': answer,
                        'correct_answer': fallback_question['correct_answer'],
                        'explanation': fallback_question['explanation']
                    })
                    st.rerun()
                
                if hint_button:
                    st.info(f"💡 **Hint:** Consider the key aspects of {st.session_state.selected_subject} and how they apply in practice.")
    
    else:
        # Assessment complete - determine level
        correct_count = sum(1 for r in st.session_state.assessment_responses if r['correct'])
        
        st.markdown("---")
        st.success("✅ Assessment Complete!")
        
        # Determine level based on performance
        if correct_count == 3:
            level = "Advanced"
            color = "🟢"
            explanation = "You have strong foundational knowledge and are ready for advanced topics!"
        elif correct_count == 2:
            level = "Intermediate"
            color = "🟡"
            explanation = "You have good understanding and can handle intermediate concepts!"
        else:
            level = "Beginner"
            color = "🔵"
            explanation = "You're building your foundation - start with basics and progress gradually!"
        
        st.session_state.student_level = level
        st.session_state.assessment_complete = True
        
        # Display level
        st.metric("Your Level", f"{color} {level}", f"Score: {correct_count}/3")
        st.write(f"**Analysis:** {explanation}")
        
        # Show performance breakdown
        st.markdown("### Performance Breakdown")
        for idx, response in enumerate(st.session_state.assessment_responses):
            status = "✅ Correct" if response['correct'] else "❌ Incorrect"
            st.write(f"**Question {idx + 1} ({response['difficulty']}):** {status}")
        
        st.markdown("---")
        
        if st.button("🚀 Start Learning", use_container_width=True, type="primary"):
            st.session_state.quiz_started = False
            st.rerun()


def render_sidebar():
    """Render sidebar navigation"""
    st.sidebar.title("🎓 Tutor Agent")
    st.sidebar.markdown("---")
    
    # Show logged in user info
    if st.session_state.logged_in:
        st.sidebar.success(f"👤 {st.session_state.student_name}")
        if st.session_state.selected_subject:
            st.sidebar.info(f"📚 Subject: {st.session_state.selected_subject}")
            if st.session_state.student_level:
                st.sidebar.info(f"📊 Level: {st.session_state.student_level}")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.selected_subject = None
            st.session_state.student_level = None
            st.session_state.assessment_complete = False
            st.rerun()
    
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Interactive Quiz", "Learning Path", "Student Analytics", "System Info"],
        disabled=not st.session_state.assessment_complete
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info(
        "**Personalized Tutor Agent**\n\n"
        "An AI-powered learning system that:\n"
        "- 🎯 Analyzes your knowledge level\n"
        "- 🤖 Uses AI for personalized feedback\n"
        "- 📈 Adapts to your learning style\n"
        "- 🎓 Generates custom learning paths"
    )
    
    return page


def render_dashboard(profile_manager, dkt, path_manager, student_id):
    """Render main dashboard"""
    st.title("📊 Personalized Tutor Dashboard")
    
    # Get student profile
    profile = profile_manager.get_or_create_profile(student_id)
    knowledge = profile.get_knowledge_state_vector()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Accuracy",
            f"{profile.overall_metrics['average_accuracy']:.1%}",
            "↑ +5%" if profile.overall_metrics['total_questions'] > 0 else None
        )
    
    with col2:
        st.metric(
            "Total Questions",
            int(profile.overall_metrics['total_questions']),
            f"+{int(profile.overall_metrics['total_questions'] // 10)}"
        )
    
    with col3:
        avg_mastery = np.mean(list(knowledge.values()))
        st.metric(
            "Average Mastery",
            f"{avg_mastery:.1%}",
            "Progressing" if avg_mastery > 0.5 else "Developing"
        )
    
    with col4:
        time_hours = profile.overall_metrics['total_time_spent'] / 3600
        st.metric(
            "Time Invested",
            f"{time_hours:.1f}h",
            "Learning Actively" if time_hours > 2 else "Just Started"
        )
    
    st.markdown("---")
    
    # Knowledge state visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Knowledge State by Concept")
        
        knowledge_df = pd.DataFrame({
            'Concept': list(knowledge.keys()),
            'Mastery': list(knowledge.values())
        })
        
        fig = px.bar(
            knowledge_df,
            x='Concept',
            y='Mastery',
            color='Mastery',
            color_continuous_scale='RdYlGn',
            range_color=(0, 1),
            height=400
        )
        fig.update_layout(
            yaxis_title="Mastery Probability",
            xaxis_title="Concept",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💪 Concept Statistics")
        
        # Strong and weak concepts
        strong = profile.get_strong_concepts(n=3)
        weak = profile.get_weak_concepts(n=3)
        
        st.markdown("#### ✅ Strong Concepts")
        for concept in strong:
            mastery = knowledge[concept]
            st.progress(mastery, text=f"{concept}: {mastery:.1%}")
        
        st.markdown("#### 📍 Areas for Improvement")
        for concept in weak:
            mastery = knowledge[concept]
            st.progress(mastery, text=f"{concept}: {mastery:.1%}")
    
    st.markdown("---")
    
    # Performance by concept
    st.subheader("📊 Performance by Concept")
    
    concept_stats = []
    for concept in knowledge.keys():
        stats = profile.get_concept_statistics(concept)
        if stats:
            concept_stats.append(stats)
    
    if concept_stats:
        stats_df = pd.DataFrame(concept_stats)
        st.dataframe(
            stats_df[['concept', 'total_attempts', 'accuracy', 'avg_time_spent', 'mastery_probability']],
            use_container_width=True,
            hide_index=True
        )
    
    # Recommendations
    st.markdown("---")
    st.subheader("🎯 Personalized Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### What to Focus On")
        for i, concept in enumerate(weak[:3], 1):
            st.write(f"{i}. **{concept}** - Mastery: {knowledge[concept]:.1%}")
            st.caption("Needs more practice. Try easier problems first.")
    
    with col2:
        st.markdown("#### Your Strengths")
        for i, concept in enumerate(strong[:3], 1):
            st.write(f"{i}. **{concept}** - Mastery: {knowledge[concept]:.1%}")
            st.caption("Great! Try harder problems or teach others.")


def render_quiz(qbank, student_id, profile_manager, tutor_agent):
    """Render interactive quiz"""
    st.title("📝 Adaptive Quiz")
    
    profile = profile_manager.get_or_create_profile(student_id)
    knowledge = profile.get_knowledge_state_vector()
    
    # Quiz setup
    col1, col2 = st.columns(2)
    
    with col1:
        concept = st.selectbox(
            "Select Concept to Practice",
            list(knowledge.keys())
        )
    
    with col2:
        difficulty_adaptor = DifficultyAdaptor('Medium')
        st.info(f"Current Difficulty: {difficulty_adaptor.current_difficulty}")
    
    # Quiz controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Start New Quiz"):
            st.session_state.quiz_started = True
            st.session_state.quiz_responses = []
            st.session_state.current_question_idx = 0
            st.session_state.current_question_data = None
            st.rerun()
    
    with col2:
        st.metric("Questions Attempted", len(st.session_state.quiz_responses))
    
    with col3:
        if st.session_state.quiz_responses:
            accuracy = np.mean([r['correct'] for r in st.session_state.quiz_responses])
            st.metric("Current Accuracy", f"{accuracy:.1%}")
    
    st.markdown("---")
    
    st.write(f"🔵 Quiz Started: {st.session_state.quiz_started}")
    st.write(f"📊 Questions Completed: {len(st.session_state.quiz_responses)}")
    
    if st.session_state.quiz_started:
        # Determine difficulty based on performance
        if len(st.session_state.quiz_responses) == 0:
            difficulty = "Easy"
        else:
            accuracy = np.mean([r['correct'] for r in st.session_state.quiz_responses])
            if accuracy >= 0.8:
                difficulty = "Hard"
            elif accuracy >= 0.5:
                difficulty = "Medium"
            else:
                difficulty = "Easy"
        
        # Get or generate current question
        if st.session_state.current_question_data is None:
            st.write("🤖 Generating AI question...")
            try:
                question_data = tutor_agent.generate_quiz_question(
                    concept=concept,
                    difficulty=difficulty,
                    mastery_level=knowledge.get(concept, 0.5)
                )
                st.session_state.current_question_data = question_data
            except Exception as e:
                st.error(f"❌ Error generating question: {e}")
                return
        
        question_data = st.session_state.current_question_data
        
        # Display question clearly
        st.subheader(f"Question {len(st.session_state.quiz_responses) + 1}")
        
        # Question metadata
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Concept", concept)
        with col2:
            st.metric("Difficulty", difficulty)
        with col3:
            st.metric("Time Limit", "60s")
        
        st.markdown("---")
        
        # THE ACTUAL QUESTION - PROMINENT DISPLAY
        st.markdown("### 📋 Question")
        st.warning(f"**{question_data['question']}**")
        
        st.markdown("---")
        
        # Answer selection using form to prevent auto-submission
        st.markdown("### 📌 Your Answer")
        with st.form(key=f"quiz_form_{len(st.session_state.quiz_responses)}", clear_on_submit=False):
            answer = st.radio(
                "Select one:",
                question_data['options'],
                key=f"q_{len(st.session_state.quiz_responses)}"
            )
            
            st.markdown("---")
            
            # Buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                submit_button = st.form_submit_button("✅ Submit Answer", use_container_width=True, type="primary")
            
            with col2:
                hint_button = st.form_submit_button("💡 Get Hint", use_container_width=True)
            
            with col3:
                end_button = st.form_submit_button("❌ End Quiz", use_container_width=True)
            
            if submit_button:
                # Check if answer is correct
                is_correct = (answer == question_data['correct_answer'])
                
                response = {
                    'question': question_data['question'],
                    'student_answer': answer,
                    'correct_answer': question_data['correct_answer'],
                    'correct': is_correct,
                    'time_spent': 45,
                    'concept': concept,
                    'difficulty': difficulty,
                    'explanation': question_data['explanation']
                }
                st.session_state.quiz_responses.append(response)
                st.session_state.current_question_data = None
                st.rerun()
            
            if hint_button:
                hint = tutor_agent.generate_hint(
                    concept=concept,
                    question=question_data['question'],
                    student_attempt=answer,
                    hint_level=1
                )
                st.info(hint)
            
            if end_button:
                st.session_state.quiz_started = False
                st.session_state.current_question_data = None
                st.rerun()
        
        st.markdown("---")
        
        # Show feedback for last response
        if st.session_state.quiz_responses:
            last_response = st.session_state.quiz_responses[-1]
            
            # Use AI-powered feedback
            feedback = tutor_agent.generate_immediate_feedback(
                is_correct=last_response['correct'],
                student_response=last_response['student_answer'],
                correct_answer=last_response['correct_answer'],
                concept=concept,
                difficulty=difficulty,
                mastery_level=knowledge.get(concept, 0.5),
                time_spent=last_response['time_spent'],
                estimated_time=60
            )
            
            st.markdown("### 📌 Feedback")
            if last_response['correct']:
                st.success("✅ Correct!")
                st.success(feedback)
                st.info(f"**Explanation:** {last_response['explanation']}")
            else:
                st.warning("❌ Incorrect")
                st.warning(feedback)
                st.info(f"**Correct Answer:** {last_response['correct_answer']}")
                st.info(f"**Explanation:** {last_response['explanation']}")
        
        # End quiz summary
        if len(st.session_state.quiz_responses) >= 5:
            st.markdown("---")
            st.subheader("Quiz Summary")
            
            accuracy = np.mean([r['correct'] for r in st.session_state.quiz_responses])
            st.metric("Quiz Accuracy", f"{accuracy:.1%}")
            
            summary = tutor_agent.create_quiz_completion_summary(
                {'accuracy': accuracy, 'total_questions': len(st.session_state.quiz_responses), 'avg_time_spent': 40},
                concept,
                [],
                profile.get_weak_concepts(n=2)
            )
            st.markdown(summary)
            
            if st.button("Take Another Quiz"):
                st.session_state.quiz_started = False
                st.rerun()


def render_learning_path(path_manager, profile_manager, student_id):
    """Render learning path"""
    st.title("🛤️ Your Personalized Learning Path")
    
    profile = profile_manager.get_or_create_profile(student_id)
    knowledge = profile.get_knowledge_state_vector()
    
    # Path generator
    path_gen = LearningPathGenerator(
        list(knowledge.keys()),
        concept_difficulty={c: np.random.uniform(0.2, 0.8) for c in knowledge.keys()}
    )
    
    # Generate path
    weak_concepts = profile.get_weak_concepts(n=3)
    path = path_gen.generate_path(
        knowledge,
        weak_concepts=weak_concepts,
        num_concepts=5,
        learning_preference='balanced'
    )
    
    if path:
        st.subheader("Recommended Learning Sequence")
        
        for node in path:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Position", node['position'])
            
            with col2:
                st.write(f"**{node['concept']}**")
            
            with col3:
                st.progress(node['current_mastery'], 
                           text=f"Mastery: {node['current_mastery']:.0%}")
            
            with col4:
                st.write(f"**{node['bloom_level']}**")
            
            with col5:
                st.write(f"⏱️ {node['estimated_time']}m")
            
            # Resources
            with st.expander("View Resources & Details"):
                st.write("**Recommended Resources:**")
                for resource in node['resources']:
                    st.write(f"• {resource}")
                st.write(f"**Prerequisites:** {', '.join(node['prerequisites']) or 'None'}")
        
        # Path summary
        st.markdown("---")
        total_time = path_gen.estimate_path_duration(path)
        st.info(f"⏱️ Estimated time to complete path: **{total_time} minutes** (~{total_time/60:.1f} hours)")
    else:
        st.warning("No learning path available. Start by taking a quiz!")


def render_analytics(profile_manager, student_id):
    """Render student analytics"""
    st.title("📈 Student Analytics")
    
    profile = profile_manager.get_or_create_profile(student_id)
    knowledge = profile.get_knowledge_state_vector()
    
    # Overview
    st.subheader("Student Profile Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**Total Questions:** {int(profile.overall_metrics['total_questions'])}")
        st.write(f"**Correct Answers:** {int(profile.overall_metrics['total_correct'])}")
    
    with col2:
        st.write(f"**Accuracy:** {profile.overall_metrics['average_accuracy']:.1%}")
        st.write(f"**Avg Mastery:** {np.mean(list(knowledge.values())):.1%}")
    
    with col3:
        time_hours = profile.overall_metrics['total_time_spent'] / 3600
        st.write(f"**Time Invested:** {time_hours:.1f} hours")
    
    st.markdown("---")
    
    # Concept mastery heatmap
    st.subheader("Concept Mastery Heatmap")
    
    concepts = list(knowledge.keys())
    masteries = [knowledge[c] for c in concepts]
    
    fig = go.Figure(data=go.Heatmap(
        z=[masteries],
        x=concepts,
        colorscale='RdYlGn',
        zmin=0,
        zmax=1
    ))
    fig.update_layout(height=200)
    st.plotly_chart(fig, use_container_width=True)
    
    # Progress over time (simulated)
    st.subheader("Learning Progress Simulation")
    
    progress_df = pd.DataFrame({
        'Question': range(1, 21),
        'Cumulative Accuracy': np.cumsum(np.random.binomial(1, 0.65, 20)) / np.arange(1, 21)
    })
    
    fig = px.line(progress_df, x='Question', y='Cumulative Accuracy',
                  title='Cumulative Accuracy Over Time',
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)


def render_system_info():
    """Render system information"""
    st.title("ℹ️ System Information")
    
    st.subheader("Project Overview")
    st.markdown("""
    ### Personalized Tutor Agent / Learning Path Generator
    
    **An AI-powered Intelligent Tutoring System with personalized learning paths**
    
    #### Key Features:
    - 🧠 **Learner Profiling**: Tracks student performance and knowledge state
    - 📊 **Knowledge Tracing**: Simplified DKT for mastery prediction
    - 🛤️ **Learning Path Generation**: Personalized, adaptive learning sequences
    - 📝 **Adaptive Quiz Engine**: Difficulty-adjusting question selection
    - 💬 **Tutor Agent**: NLP-based feedback, hints, and encouragement
    - 📱 **Interactive UI**: Real-time learning analytics and guidance
    
    #### Technologies:
    - **Backend**: Python, Pandas, NumPy, Scikit-learn
    - **Learning**: Simplified DKT, Bayesian Knowledge Tracing
    - **NLP**: Rule-based feedback generation
    - **Frontend**: Streamlit
    """)
    
    st.markdown("---")
    
    st.subheader("Architecture")
    
    arch = """
    ```
    ┌─────────────────────────────────────────┐
    │    Streamlit User Interface              │
    │  (Dashboard, Quiz, Analytics)            │
    └──────────────┬──────────────────────────┘
                   │
    ┌──────────────┴──────────────────────────┐
    │    Personalized Tutor Agent             │
    │  - Feedback Generator                   │
    │  - Hint System                          │
    │  - Motivational Messages                │
    └──────────────┬──────────────────────────┘
                   │
    ┌──────────────┴──────────────────────────┐
    │    Core Learning Modules                │
    │  1. Learner Profiling                   │
    │  2. Knowledge Tracing (DKT)             │
    │  3. Learning Path Generator             │
    │  4. Adaptive Quiz Engine                │
    └──────────────┬──────────────────────────┘
                   │
    ┌──────────────┴──────────────────────────┐
    │    Data Layer                           │
    │  - Student Interactions                 │
    │  - Question Bank                        │
    │  - Concept Relationships                │
    └─────────────────────────────────────────┘
    ```
    """
    st.code(arch, language='text')
    
    st.markdown("---")
    
    st.subheader("Research References")
    st.markdown("""
    - **Deep Knowledge Tracing** - Piech et al., NeurIPS 2015
    - **Item Response Theory** - Birnbaum, 1968
    - **Adaptive Learning** - Bloom, 1984
    - **Personalization in Education** - IEEE Educational Data Mining
    - **Intelligent Tutoring Systems** - Springer Handbook of AI in Education
    """)
    
    st.markdown("---")
    
    st.subheader("Dataset Information")
    st.markdown("""
    **Synthetic Dataset Generated:**
    - 50 students
    - 8 learning concepts
    - 80 unique questions
    - 3,000 student-question interactions
    
    Fields: student_id, concept, question_id, difficulty, score, time_spent, attempt_no, timestamp
    """)


def main():
    """Main Streamlit app"""
    
    # Initialize session
    manager = TutorSessionManager()
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        render_login_page()
        return
    
    # Load data
    interactions_df, qbank_df = load_data()
    
    if interactions_df is None or qbank_df is None:
        st.error("Cannot start application without data files.")
        return
    
    # Check if subject is selected
    if not st.session_state.selected_subject:
        render_subject_selection()
        return
    
    # Initialize managers
    concepts = interactions_df['concept'].unique().tolist()
    
    profile_manager = LearnerProfileManager(concepts)
    profile_manager.update_from_interactions(interactions_df)
    
    dkt = SimplifiedDKT(concepts)
    
    path_manager = AdaptivePathManager(
        LearningPathGenerator(concepts)
    )
    
    qbank = QuestionBank(qbank_df)
    
    tutor_agent = PersonalizedTutorAgent()
    
    # Check if initial assessment is complete
    if not st.session_state.assessment_complete:
        render_initial_assessment(tutor_agent, qbank, profile_manager, st.session_state.student_id)
        return
    
    # Render sidebar (only after login and assessment)
    page = render_sidebar()
    
    # Route pages
    if page == "Dashboard":
        render_dashboard(profile_manager, dkt, path_manager, st.session_state.student_id)
    
    elif page == "Interactive Quiz":
        render_quiz(qbank, st.session_state.student_id, profile_manager, tutor_agent)
    
    elif page == "Learning Path":
        render_learning_path(path_manager, profile_manager, st.session_state.student_id)
    
    elif page == "Student Analytics":
        render_analytics(profile_manager, st.session_state.student_id)
    
    elif page == "System Info":
        render_system_info()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>© 2024 Personalized Tutor Agent | "
        "AI-Powered Learning with Groq</p>",
        unsafe_allow_html=True
    )


if __name__ == '__main__':
    main()
