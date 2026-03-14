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
import time
import logging
import sys
import os

logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from learner_profiling import LearnerProfileManager
from knowledge_tracing import SimplifiedDKT
from learning_path import LearningPathGenerator, AdaptivePathManager
from tutor_agent import PersonalizedTutorAgent
from src.courses import CourseManager
from learning_content import LearningContentGenerator, LearningPathOrchestrator
from src.curriculum import Curriculum
from src.structured_learning import StructuredLearningManager, StructuredLearningSession

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
        st.session_state.selected_course = None
        st.session_state.student_level = None  # beginner, intermediate, advanced
        st.session_state.assessment_complete = False
        st.session_state.learning_path_displayed = False
        st.session_state.quiz_started = False
        st.session_state.quiz_responses = []
        st.session_state.quiz_concept = None  # Track which topic's quiz is being taken
        st.session_state.learning_session = None
        st.session_state.recent_performance = {}
        st.session_state.learning_materials_viewed = []
        st.session_state.learning_path = []
        st.session_state.knowledge_state = {}
        st.session_state.interaction_data = None
        st.session_state.current_question_idx = 0
        st.session_state.assessment_responses = []
        st.session_state.current_question_data = None
        # Structured learning session state
        st.session_state.structured_learning_session = None
        st.session_state.current_topic_step = "explanation"  # explanation, examples, quiz_prompt, quiz, completed
        # Learning Path tracking
        st.session_state.current_concept_idx = 0  # Track which concept user is on
        st.session_state.concepts_list = []  # List of 10 concepts for current level/subject
        st.session_state.concept_completion_status = {}  # Track completion status per concept
        st.session_state.quiz_question_index = 0
        st.session_state.current_page = None  # Track current page for button-based navigation (None = use sidebar)
        st.session_state.quiz_topic_responses = []
        st.session_state.quiz_questions = []
        # Assessment feedback tracking
        st.session_state.current_assessment_question = None  # Question data after answer submitted
        st.session_state.current_question_for_assessment = None  # Question data before answer submitted
        st.session_state.showing_assessment_feedback = False
        st.session_state.assessment_answer_submitted = None



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
    subjects = ["Mathematics", "Physics", "Chemistry"]
    
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
    
    st.markdown("---")
    st.success("📚 **More courses coming soon!** Stay tuned for Biology, History, Geography, and more exciting subjects!")


def render_initial_assessment(tutor_agent, profile_manager, student_id):
    """Render initial assessment to determine student level with inline feedback"""
    st.title(f"📋 Initial Assessment - {st.session_state.selected_subject}")
    st.subheader("Let's analyze your knowledge level...")
    
    # Difficulty progression for assessment
    assessment_difficulties = ["Easy", "Easy-Medium", "Medium", "Medium-Hard", "Hard"]
    
    st.markdown(f"Answer **5 quick questions** to determine your level...")
    st.progress(len(st.session_state.assessment_responses) / 5)
    st.write(f"📊 Progress: {len(st.session_state.assessment_responses)}/5 completed")
    
    if len(st.session_state.assessment_responses) >= 5:
        # Assessment complete - determine level
        correct_count = sum(1 for r in st.session_state.assessment_responses if r['correct'])
        
        st.markdown("---")
        st.success("✅ Assessment Complete!")
        
        # Determine level based on performance (out of 5 questions)
        if correct_count >= 4:
            level = "Advanced"
            color = "🟢"
            explanation = "You have strong foundational knowledge and are ready for advanced topics!"
        elif correct_count >= 3:
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
        st.metric("Your Level", f"{color} {level}", f"Score: {correct_count}/5")
        st.write(f"**Analysis:** {explanation}")
        
        # Show performance breakdown
        st.markdown("### Performance Breakdown")
        for idx, response in enumerate(st.session_state.assessment_responses):
            status = "✅ Correct" if response['correct'] else "❌ Incorrect"
            st.write(f"**Question {idx + 1} ({response['difficulty']}):** {status}")
        
        st.markdown("---")
        
        # Auto-generate learning path immediately
        st.info("🚀 Generating your personalized learning path...")
        try:
            from learning_content import LearningPathOrchestrator
            orchestrator = LearningPathOrchestrator()
            
            course = CourseManager.get_course(st.session_state.selected_course)
            student_knowledge = profile_manager.get_or_create_profile(student_id).get_knowledge_state_vector()
            
            # Build recent performance from assessment
            recent_performance = {}
            for concept in course.concepts:
                recent_acc = correct_count / 5 if len(st.session_state.assessment_responses) > 0 else 0.5
                recent_performance[concept] = recent_acc
            
            learning_session = orchestrator.create_personalized_learning_session(
                course_id=st.session_state.selected_course,
                course_concepts=course.concepts,
                student_knowledge=student_knowledge,
                student_level=level.lower(),
                recent_performance=recent_performance
            )
            st.session_state.learning_session = learning_session
            st.session_state.learning_path_displayed = True
            st.success("✅ Learning path generated! Redirecting...")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error generating learning path: {str(e)}")
            if st.button("Try Again"):
                st.rerun()
        return
    
    # Still have more questions to answer
    current_idx = len(st.session_state.assessment_responses)
    difficulty = assessment_difficulties[current_idx]
    
    # Load or generate the current question (cache it to avoid regenerating)
    if st.session_state.current_question_for_assessment is None or st.session_state.current_question_for_assessment.get('_question_idx', -1) != current_idx:
        # Generate new question only if we don't have one cached or the index changed
        st.write("🤖 Generating AI question...")
        try:
            question_data = tutor_agent.generate_quiz_question(
                concept=st.session_state.selected_subject,
                difficulty=difficulty,
                mastery_level=0.5
            )
        except Exception as e:
            st.error(f"❌ Error generating question: {e}")
            st.write("Using fallback question...")
            
            # Fallback question
            question_data = {
                "question": f"What is a key aspect of {st.session_state.selected_subject}?",
                "options": ["Implementation", "Theory", "Practice", "Examples"],
                "correct_answer": "Practice",
                "explanation": "Practice is essential for mastering any concept."
            }
        
        # Add index tracking to question data
        question_data['_question_idx'] = current_idx
        # Cache the question
        st.session_state.current_question_for_assessment = question_data
    else:
        # Use cached question
        question_data = st.session_state.current_question_for_assessment
    
    # Don't show the form/question if we're already showing feedback
    if not st.session_state.showing_assessment_feedback:
        st.markdown("---")
        
        # Display question prominently
        st.markdown(f"### 📋 Question {current_idx + 1}")
        st.warning(f"**{question_data['question']}**")
        st.info(f"**Difficulty:** {difficulty}")
        
        st.markdown("---")
        
        # Initialize hint storage in session state if not present
        if 'assessment_hint_shown' not in st.session_state:
            st.session_state.assessment_hint_shown = {}
        if 'assessment_hints' not in st.session_state:
            st.session_state.assessment_hints = {}
        
        # Display hint if it has been generated
        if current_idx in st.session_state.assessment_hints:
            st.success(f"💡 **Hint:** {st.session_state.assessment_hints[current_idx]}")
        
        # Answer selection using a form
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
                # Save the submitted answer and mark feedback should be shown
                st.session_state.assessment_answer_submitted = answer
                st.session_state.showing_assessment_feedback = True
                # Store the question that was answered
                st.session_state.current_assessment_question = question_data
                st.rerun()
            
            if hint_button:
                # Generate AI hint specific to the question
                if current_idx not in st.session_state.assessment_hints:
                    try:
                        generated_hint = tutor_agent.generate_hint(
                            concept=st.session_state.selected_subject,
                            question=question_data['question'],
                            student_attempt="",
                            hint_level=1,
                            attempt_number=1
                        )
                        st.session_state.assessment_hints[current_idx] = generated_hint
                    except Exception as e:
                        logger.error(f"Error generating hint: {e}")
                        st.session_state.assessment_hints[current_idx] = f"💡 Think about the key concepts of {st.session_state.selected_subject} and how they relate to this question."
                
                st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.showing_assessment_feedback and st.session_state.assessment_answer_submitted:
        st.markdown("---")
        
        # Use the question that was actually answered
        question_data = st.session_state.current_assessment_question
        student_answer = st.session_state.assessment_answer_submitted
        is_correct = (student_answer == question_data['correct_answer'])
        
        # Display correct/incorrect feedback
        if is_correct:
            st.success("✅ **Correct!**")
            st.markdown(f"Great job! You selected the right answer.")
        else:
            st.error("❌ **Incorrect**")
            st.markdown(f"""
I can see you're making an effort to understand this topic, and that's something to be proud of. Your answer, "{student_answer}," isn't quite correct because the question is asking about {st.session_state.selected_subject}. Let's focus on understanding the key concepts better to improve your understanding.
            """)
        
        # Display correct answer
        st.markdown("---")
        st.info(f"**Correct Answer:** {question_data['correct_answer']}")
        
        # Display explanation
        explanation = str(question_data.get('explanation', 'No explanation available.')).split('main()')[0].strip()
        st.markdown(f"**Explanation:** {explanation}")
        
        st.markdown("---")
        
        # Next question button or Generate Learning Path for 5th question
        is_last_question = (current_idx == 4)  # 5th question (0-indexed)
        button_text = "🚀 Generate Learning Path" if is_last_question else "📝 Next Question →"
        
        if st.button(button_text, use_container_width=True, type="primary", key=f"next_assessment_{current_idx}"):
            # Save response
            st.session_state.assessment_responses.append({
                'question_id': f'assess_{current_idx + 1}',
                'difficulty': difficulty,
                'correct': is_correct,
                'question': str(question_data['question']),
                'student_answer': student_answer,
                'correct_answer': str(question_data['correct_answer']),
                'explanation': explanation
            })
            
            # Reset feedback state
            st.session_state.showing_assessment_feedback = False
            st.session_state.assessment_answer_submitted = None
            st.session_state.current_assessment_question = None
            st.session_state.current_question_for_assessment = None  # Clear cache for next question
            # Don't clear hints in case user wants to review them
            st.rerun()



def render_learning_path_post_assessment():
    """Render personalized learning path after assessment"""
    st.title("📚 Your Personalized Learning Path")
    
    try:
        # Check if learning session exists in state
        if st.session_state.learning_session:
            learning_session = st.session_state.learning_session
        else:
            # If not, check for course and regenerate
            if not st.session_state.selected_course:
                st.error("❌ No course selected. Please select a course first.")
                return
            
            course = CourseManager.get_course(st.session_state.selected_course)
            if not course:
                st.error("❌ Course not found. Please select a course.")
                return
            
            st.warning("Regenerating learning path...")
            from learning_content import LearningPathOrchestrator
            orchestrator = LearningPathOrchestrator()
            
            student_id = st.session_state.student_id
            profile_manager = LearnerProfileManager()
            profile = profile_manager.get_or_create_profile(student_id)
            student_knowledge = profile.get_knowledge_state_vector()
            
            recent_performance = {}
            for concept in course.concepts:
                recent_acc = sum(
                    1 for r in st.session_state.assessment_responses if r['correct']
                ) / len(st.session_state.assessment_responses) if st.session_state.assessment_responses else 0.5
                recent_performance[concept] = recent_acc
            
            learning_session = orchestrator.create_personalized_learning_session(
                course_id=st.session_state.selected_course,
                course_concepts=course.concepts,
                student_knowledge=student_knowledge,
                student_level=st.session_state.student_level.lower() if st.session_state.student_level else "beginner",
                recent_performance=recent_performance
            )
            st.session_state.learning_session = learning_session
        
        # Get course info
        course = CourseManager.get_course(st.session_state.selected_course)
        if not course:
            st.error("❌ Course not found.")
            return
        
        # Display session summary
        st.success("✅ Learning Path Generated!")
        
        st.markdown(f"""
        ## 🎓 Your Recommended Learning Sequence
        
        Based on your **{st.session_state.student_level}** level and recent performance, 
        we've created a personalized path through **{course.name}**.
        
        **Total Estimated Time:** ⏱️ {learning_session['estimated_total_time']} minutes (~{learning_session['estimated_total_time']/60:.1f} hours)
        """)
        
        st.markdown("---")
        
        # Display learning materials
        st.subheader("📚 Recommended Learning Materials")
        
        for idx, item in enumerate(learning_session["learning_materials"]):
            rec = item["recommendation"]
            mat = item["material"]
            
            with st.expander(
                f"**{idx + 1}. {rec.concept.capitalize()}** ({mat.material_type.capitalize()}) - {mat.duration_minutes}min",
                expanded=(idx == 0)
            ):
                # Recommendation reason
                st.write(f"**📌 Why this?** {rec.reason}")
                st.write(f"**⏱️ Estimated time:** {mat.duration_minutes} minutes")
                st.write(f"**📖 Type:** {mat.material_type.capitalize()}")
                
                st.markdown("---")
                
                # Display content
                st.write(f"### {mat.title}")
                st.write(mat.content)
                
                st.markdown("---")
                
                # Mark as viewed
                if st.button(f"✅ Mark as Complete", key=f"complete_{idx}"):
                    st.session_state.learning_materials_viewed.append(rec.concept)
                    st.success(f"Great! You've completed {rec.concept}. Ready for the next topic?")
        
        # Progress indicator
        st.markdown("---")
        st.subheader("📊 Your Progress")
        
        materials_viewed = len(st.session_state.learning_materials_viewed)
        total_materials = len(learning_session["learning_materials"])
        progress = materials_viewed / total_materials if total_materials > 0 else 0
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(progress)
        with col2:
            st.write(f"{materials_viewed}/{total_materials} completed")
        
        st.markdown("---")
        
        # Next steps
        st.info(f"""
        **💡 Next Steps:**
        
        1. 📖 Start with the **{learning_session['learning_materials'][0]['recommendation'].concept.capitalize()}** concept
        2. 📝 Review the learning material and examples
        3. ✍️ Work through the practice problems
        4. 🎯 When ready, take a quiz to test your understanding
        5. 🔄 Repeat with the next recommended concept
        
        **Remember:** Learning is a journey, not a race. Take your time and understand each concept deeply!
        """)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Take a Quiz", use_container_width=True):
                st.session_state.learning_path_displayed = False
                st.session_state.quiz_started = True
                st.rerun()
        
        with col2:
            if st.button("📊 View Dashboard", use_container_width=True):
                st.session_state.learning_path_displayed = False
                st.rerun()
        
        with col3:
            if st.button("🔄 Regenerate Path", use_container_width=True):
                st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error generating learning path: {str(e)}")
        import traceback
        st.error(traceback.format_exc())


def render_structured_learning_flow():
    """Render the new structured learning flow with topics, explanations, examples, and quizzes"""
    st.title("📚 Structured Learning Path")
    
    # Top Navigation Bar
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 1, 1, 2])
    with nav_col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.structured_learning_session = None
            st.session_state.learning_path_displayed = False
            st.rerun()
    with nav_col2:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.learning_path_displayed = False
            st.rerun()
    with nav_col3:
        if st.button("🔄 Restart", use_container_width=True):
            st.session_state.structured_learning_session = None
            st.session_state.current_topic_step = "explanation"
            st.rerun()
    
    st.markdown("---")
    
    try:
        # Initialize structured learning manager
        content_generator = LearningContentGenerator()
        learning_manager = StructuredLearningManager(content_generator)
        
        # Create or retrieve session
        selected_concept_idx = None
        
        if not st.session_state.structured_learning_session:
            # No session exists, create new one
            session = learning_manager.create_session(
                subject=st.session_state.selected_subject,
                student_level=st.session_state.student_level.lower() if st.session_state.student_level else "beginner"
            )
            st.session_state.structured_learning_session = session
        elif isinstance(st.session_state.structured_learning_session, dict):
            # This is a dict from concept selection in Learning Path - convert to proper session
            selected_concept_idx = st.session_state.structured_learning_session.get('concept_index', 0)
            session = learning_manager.create_session(
                subject=st.session_state.selected_subject,
                student_level=st.session_state.student_level.lower() if st.session_state.student_level else "beginner"
            )
            # Move to the selected concept
            if selected_concept_idx > 0 and selected_concept_idx < len(session.topics):
                # Skip to the selected topic by updating completed_topics counter
                session.completed_topics = selected_concept_idx
            st.session_state.structured_learning_session = session
        else:
            # Proper session object exists
            session = st.session_state.structured_learning_session
        
        # Check if all topics are completed
        if session.is_completed():
            st.success("🎉 Congratulations! You've completed all topics in this learning path!")
            
            # Show summary
            summary = learning_manager.get_session_summary(session)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Topics", summary['total_topics'])
            with col2:
                st.metric("Completed", summary['completed_topics'])
            with col3:
                st.metric("Progress", f"{summary['progress_percentage']:.0f}%")
            with col4:
                st.metric("Avg Quiz Score", f"{summary['average_quiz_score']:.1f}%")
            
            st.markdown("---")
            
            if st.button("🔄 Start New Learning Path", use_container_width=True):
                st.session_state.structured_learning_session = None
                st.session_state.current_topic_step = "explanation"
                st.rerun()
            
            if st.button("📊 View Dashboard", use_container_width=True):
                st.session_state.learning_path_displayed = False
                st.rerun()
            
            return
        
        # Display progress
        current_topic = session.get_current_topic()
        if not current_topic:
            st.error("❌ No current topic")
            return
        
        # Progress bar
        progress_percentage = session.get_progress_percentage()
        st.progress(progress_percentage / 100)
        st.caption(f"Progress: {session.completed_topics}/{len(session.topics)} topics ({progress_percentage:.0f}%)")
        
        st.markdown(f"### Topic {session.completed_topics + 1}/{len(session.topics)}: {current_topic.name}")
        st.markdown(f"**Level:** {session.student_level.capitalize()} | **Subject:** {session.subject}")
        st.markdown(f"*{current_topic.description}*")
        st.markdown("---")
        
        # Step 1: Explanation
        if st.session_state.current_topic_step == "explanation":
            st.subheader("📖 Concept Explanation")
            
            with st.spinner(f"Loading explanation for {current_topic.name}..."):
                explanation_result = learning_manager.load_topic_explanation(session)
            
            if "error" not in explanation_result:
                st.markdown(explanation_result['explanation'])
            else:
                st.error(f"Error loading explanation: {explanation_result['error']}")
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("➡️ Next: Examples", use_container_width=True):
                    st.session_state.current_topic_step = "examples"
                    st.rerun()
        
        # Step 2: Examples
        elif st.session_state.current_topic_step == "examples":
            st.subheader("💡 Practical Examples")
            
            with st.spinner(f"Loading examples for {current_topic.name}..."):
                examples_result = learning_manager.load_topic_examples(session)
            
            if "error" not in examples_result:
                st.markdown(examples_result['examples'])
            else:
                st.error(f"Error loading examples: {examples_result['error']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⬅️ Back: Explanation", use_container_width=True):
                    st.session_state.current_topic_step = "explanation"
                    st.rerun()
            
            with col3:
                if st.button("➡️ Next: Quiz", use_container_width=True):
                    st.session_state.current_topic_step = "quiz_prompt"
                    st.rerun()
        
        # Step 3: Quiz Prompt
        elif st.session_state.current_topic_step == "quiz_prompt":
            st.subheader("🎯 Quiz Time!")
            
            st.info(f"""
            You've learned about **{current_topic.name}**. Now let's test your understanding!
            
            **Ready to take a quiz on this topic?**
            """)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✅ Yes, Take Quiz", use_container_width=True, key="take_quiz_yes"):
                    learning_manager.record_quiz_completion(session, quiz_taken=True)
                    st.session_state.current_topic_step = "quiz"
                    st.session_state.quiz_started = True
                    st.session_state.quiz_question_index = 0
                    st.session_state.quiz_topic_responses = []
                    st.rerun()
            
            with col2:
                if st.button("⏭️ Skip Quiz", use_container_width=True, key="skip_quiz"):
                    learning_manager.record_quiz_completion(session, quiz_taken=False)
                    session.move_to_next_topic()
                    
                    # Update concept tracking
                    if st.session_state.concepts_list and st.session_state.current_concept_idx < len(st.session_state.concepts_list):
                        current_topic_obj = st.session_state.concepts_list[st.session_state.current_concept_idx]
                        st.session_state.concept_completion_status[current_topic_obj.id] = True
                        st.session_state.current_concept_idx += 1
                    
                    st.session_state.current_topic_step = "explanation"
                    st.rerun()
            
            with col3:
                if st.button("⬅️ Back: Examples", use_container_width=True):
                    st.session_state.current_topic_step = "examples"
                    st.rerun()
        
        # Step 4: Quiz (adaptive with real questions)
        elif st.session_state.current_topic_step == "quiz":
            st.subheader(f"📝 Quiz: {current_topic.name}")
            
            # Initialize quiz session state if needed
            if 'quiz_question_index' not in st.session_state:
                st.session_state.quiz_question_index = 0
            if 'quiz_topic_responses' not in st.session_state:
                st.session_state.quiz_topic_responses = []
            if 'quiz_questions' not in st.session_state:
                st.session_state.quiz_questions = []
            
            # Generate quiz questions on first load
            if len(st.session_state.quiz_questions) == 0:
                st.info("🔄 Generating personalized quiz questions for this topic...")
                
                # Initialize tutor agent
                tutor_agent = PersonalizedTutorAgent()
                
                # Map difficulty level
                difficulty_map = {
                    "beginner": "Easy",
                    "intermediate": "Medium",
                    "advanced": "Hard"
                }
                difficulty = difficulty_map.get(st.session_state.student_level.lower(), "Medium")
                
                # Generate 3 quiz questions specifically for this topic
                topic_questions = []
                for i in range(3):
                    try:
                        question_data = tutor_agent.generate_quiz_question(
                            concept=current_topic.name,
                            difficulty=difficulty,
                            mastery_level=0.5
                        )
                        topic_questions.append(question_data)
                    except Exception as e:
                        logger.error(f"Error generating question {i+1}: {e}")
                        # Fallback question
                        topic_questions.append({
                            'question': f"What is a key characteristic of {current_topic.name}?",
                            'options': [
                                'It involves understanding core principles',
                                'It is only theoretical',
                                'It has no practical applications',
                                'It is not important'
                            ],
                            'correct_answer': 'It involves understanding core principles',
                            'explanation': f"{current_topic.name} is fundamental to understanding {session.subject}"
                        })
                
                st.session_state.quiz_questions = topic_questions
                st.rerun()
            
            num_questions = len(st.session_state.quiz_questions)
            
            if st.session_state.quiz_question_index < num_questions:
                current_q_idx = st.session_state.quiz_question_index
                question_data = st.session_state.quiz_questions[current_q_idx]
                
                st.write(f"**Question {current_q_idx + 1}/{num_questions}**")
                st.write(f"Topic: **{current_topic.name}**")
                st.markdown("---")
                st.write(f"### {question_data['question']}")
                
                st.markdown("---")
                
                # Display options in form to properly manage state
                with st.form(key=f"topic_quiz_form_{current_q_idx}", clear_on_submit=False):
                    selected_answer = st.radio(
                        "Choose your answer:",
                        question_data['options'],
                        key=f"quiz_q_{current_q_idx}"
                    )
                    
                    st.markdown("---")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        submit_button = st.form_submit_button("✓ Submit Answer", use_container_width=True, type="primary")
                    
                    with col2:
                        skip_button = st.form_submit_button("⏭️ Skip Question", use_container_width=True)
                    
                    if submit_button:
                        is_correct = selected_answer == question_data['correct_answer']
                        st.session_state.quiz_topic_responses.append({
                            'question': question_data['question'],
                            'answer': selected_answer,
                            'correct': is_correct,
                            'correct_answer': question_data['correct_answer'],
                            'explanation': question_data.get('explanation', '')
                        })
                        
                        if is_correct:
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Incorrect. The correct answer is: {question_data['correct_answer']}")
                        
                        st.session_state.quiz_question_index += 1
                        time.sleep(1.5)
                        st.rerun()
                    
                    if skip_button:
                        st.session_state.quiz_topic_responses.append({
                            'question': question_data['question'],
                            'answer': 'skipped',
                            'correct': False,
                            'correct_answer': question_data['correct_answer'],
                            'explanation': question_data.get('explanation', '')
                        })
                        st.session_state.quiz_question_index += 1
                        st.rerun()
            
            else:
                # Quiz complete - show results
                st.success("🎉 Quiz Complete!")
                
                correct = sum(1 for r in st.session_state.quiz_topic_responses if r['correct'])
                total = len(st.session_state.quiz_topic_responses)
                score = (correct / total * 100) if total > 0 else 0
                
                # Display score with color coding
                if score >= 80:
                    score_color = "green"
                    score_msg = "🌟 Excellent!"
                elif score >= 60:
                    score_color = "orange"
                    score_msg = "👍 Good!"
                else:
                    score_color = "red"
                    score_msg = "📚 Keep learning!"
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Your Score", f"{score:.0f}%", f"{score_msg}")
                with col2:
                    st.metric("Correct Answers", f"{correct}/{total}")
                
                # Show answer review
                with st.expander("📋 Review Your Answers", expanded=True):
                    for idx, response in enumerate(st.session_state.quiz_topic_responses):
                        status = "✅" if response['correct'] else "❌"
                        st.write(f"**{status} Question {idx + 1}**")
                        st.write(f"📝 {response['question']}")
                        st.write(f"Your answer: **{response['answer']}**")
                        if not response['correct']:
                            st.write(f"Correct answer: **{response['correct_answer']}**")
                        if response.get('explanation'):
                            st.info(f"💡 {response['explanation']}")
                        st.markdown("---")
                
                # Record the score in session
                learning_manager.record_quiz_completion(session, quiz_taken=True, score=score)
                
                # Next steps
                st.markdown("---")
                st.subheader("What's Next?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("➡️ Next Topic", use_container_width=True, key="next_topic_btn"):
                        # Update concept tracking before moving to next
                        if st.session_state.concepts_list and st.session_state.current_concept_idx < len(st.session_state.concepts_list):
                            current_topic_obj = st.session_state.concepts_list[st.session_state.current_concept_idx]
                            st.session_state.concept_completion_status[current_topic_obj.id] = True
                            st.session_state.current_concept_idx += 1
                        
                        session.move_to_next_topic()
                        st.session_state.current_topic_step = "explanation"
                        st.session_state.quiz_question_index = 0
                        st.session_state.quiz_topic_responses = []
                        st.session_state.quiz_questions = []
                        st.rerun()
                with col2:
                    if st.button("📊 View Dashboard", use_container_width=True, key="dashboard_btn"):
                        st.session_state.learning_path_displayed = False
                        st.rerun()
    
    except Exception as e:
        st.error(f"❌ Error in structured learning: {str(e)}")
        import traceback
        st.error(traceback.format_exc())


def render_dashboard_post_assessment():
    """Render dashboard with learning recommendations"""
    st.title("📊 Dashboard")
    
    try:
        course = CourseManager.get_course(st.session_state.selected_course)
        if not course:
            st.error("❌ Course not found.")
            return
        
        # Display course overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📖 Current Course", course.name)
        with col2:
            st.metric("📊 Your Level", st.session_state.student_level)
        with col3:
            # Calculate concepts completed
            concepts_completed = sum(1 for v in st.session_state.concept_completion_status.values() if v)
            st.metric("✅ Concepts Completed", concepts_completed)
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Continue Learning", use_container_width=True):
                # Get the current concept to resume from
                if st.session_state.concepts_list:
                    current_topic = st.session_state.concepts_list[st.session_state.current_concept_idx]
                    st.session_state.structured_learning_session = {
                        'topic': current_topic,
                        'concept_index': st.session_state.current_concept_idx,
                        'started_at': str(pd.Timestamp.now())
                    }
                    st.session_state.current_topic_step = "explanation"
                    st.session_state.learning_path_displayed = True
                st.rerun()
        
        with col2:
            if st.button("📝 Take a Quiz", use_container_width=True):
                st.session_state.current_page = "Interactive Quiz"
                st.rerun()
        
        with col3:
            if st.button("🛤️ View All Concepts", use_container_width=True):
                st.session_state.current_page = "Learning Path"
                st.rerun()
        
        st.markdown("---")
        
        # Display learning session info if available
        if st.session_state.learning_session:
            st.subheader("📈 Current Learning Session")
            session = st.session_state.learning_session
            
            st.info(f"""
            **Progress:** {len(st.session_state.learning_materials_viewed)}/{len(session['learning_materials'])} materials completed
            
            **Estimated Remaining Time:** ⏱️ {session['estimated_total_time']} minutes
            
            **Next Topics:** {', '.join([item['recommendation'].concept.capitalize() for item in session['learning_materials'][:3]])}
            """)
        
        # Show current concept info
        if st.session_state.concepts_list and len(st.session_state.concepts_list) > 0:
            current_topic = st.session_state.concepts_list[st.session_state.current_concept_idx]
            st.subheader("📚 Current Learning Path")
            st.info(f"""
            **Current Topic:** {current_topic.name}
            
            **Description:** {current_topic.description}
            
            **Progress:** {st.session_state.current_concept_idx + 1}/{len(st.session_state.concepts_list)} concepts
            """)
    
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {str(e)}")



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
        ["Dashboard", "Interactive Quiz", "Learning Path", "Student Analytics", "Learning Overview"],
        disabled=not st.session_state.assessment_complete,
        key="sidebar_nav_radio"
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


def render_quiz(student_id, profile_manager, tutor_agent):
    """Render interactive quiz with topic-based unlocking"""
    st.title("📝 Interactive Quiz")
    
    # Get concepts for current subject and level
    subject = st.session_state.selected_subject
    level = st.session_state.student_level
    
    if not subject or not level:
        st.warning("⚠️ Please complete the assessment first to take a quiz.")
        return
    
    # Get the curriculum concepts for this subject and level
    from src.curriculum import Curriculum
    
    curriculum_data = None
    if subject == "Mathematics":
        curriculum_data = Curriculum.MATHEMATICS.get(level.lower())
    elif subject == "Physics":
        curriculum_data = Curriculum.PHYSICS.get(level.lower())
    elif subject == "Chemistry":
        curriculum_data = Curriculum.CHEMISTRY.get(level.lower())
    
    if not curriculum_data:
        st.error(f"❌ No curriculum found for {subject} at {level} level.")
        return
    
    # Update session concepts list if not already done
    if not st.session_state.concepts_list:
        st.session_state.concepts_list = curriculum_data
    
    # Initialize completion status if empty
    if not st.session_state.concept_completion_status:
        st.session_state.concept_completion_status = {topic.id: False for topic in curriculum_data}
    
    # Display quiz overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Subject", subject)
    with col2:
        st.metric("📊 Level", level)
    with col3:
        completed = sum(1 for v in st.session_state.concept_completion_status.values() if v)
        st.metric("✅ Completed", f"{completed}/{len(curriculum_data)}")
    
    st.markdown("---")
    
    # If quiz is not started, show topic selection
    if not st.session_state.quiz_started:
        st.subheader("📖 Select a Topic to Take Quiz")
        st.markdown("Complete topics in order to unlock new quizzes")
        
        # Display all topics with quiz buttons
        for idx, topic in enumerate(curriculum_data, 1):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            is_completed = st.session_state.concept_completion_status.get(topic.id, False)
            is_current = len(st.session_state.concepts_list) > 0 and topic.id == st.session_state.concepts_list[st.session_state.current_concept_idx].id
            topic_index = idx - 1  # 0-based index
            current_index = st.session_state.current_concept_idx
            
            # Determine status icon
            if is_current:
                status_icon = "▶️"
            elif is_completed:
                status_icon = "✅"
            else:
                status_icon = "⭕"
            
            with col1:
                display_text = f"{status_icon} [**{idx}**] {topic.name}"
                st.write(display_text)
            
            with col2:
                st.write(f"*{topic.level.capitalize()}*")
            
            with col3:
                # Determine button text and behaviour based on status
                if is_current:
                    # Current topic - show Take Quiz button
                    if st.button(f"📝 Take Quiz", use_container_width=True, key=f"quiz_btn_{topic.id}"):
                        st.session_state.quiz_started = True
                        st.session_state.quiz_concept = topic.name
                        st.session_state.quiz_responses = []
                        st.session_state.current_question_data = None
                        st.rerun()
                
                elif is_completed:
                    # Completed topic - show Retake Quiz button
                    if st.button(f"🔄 Retake Quiz", use_container_width=True, key=f"quiz_btn_{topic.id}"):
                        st.session_state.quiz_started = True
                        st.session_state.quiz_concept = topic.name
                        st.session_state.quiz_responses = []
                        st.session_state.current_question_data = None
                        st.rerun()
                
                else:
                    # Topics not yet unlocked - show lock message
                    st.button(f"🔒 Finish topic {current_index + 1}", use_container_width=True, disabled=True, key=f"quiz_btn_{topic.id}")
    
    else:
        # Quiz is in progress
        profile = profile_manager.get_or_create_profile(student_id)
        knowledge = profile.get_knowledge_state_vector()
        concept = st.session_state.quiz_concept if hasattr(st.session_state, 'quiz_concept') else st.session_state.selected_subject
        
        st.subheader(f"🎯 Quiz: {concept}")
        
        # Quiz controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Questions Attempted", len(st.session_state.quiz_responses))
        
        with col2:
            if st.session_state.quiz_responses:
                accuracy = np.mean([r['correct'] for r in st.session_state.quiz_responses])
                st.metric("Current Accuracy", f"{accuracy:.1%}")
        
        with col3:
            if st.button("❌ End Quiz", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.current_question_data = None
                st.rerun()
        
        st.markdown("---")
        
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
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Topic", concept)
        with col2:
            st.metric("Difficulty", difficulty)
        
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
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Take Another Quiz"):
                    st.session_state.quiz_started = False
                    st.rerun()
            with col2:
                if st.button("📊 Back to Dashboard"):
                    st.session_state.current_page = "Dashboard"
                    st.session_state.quiz_started = False
                    st.rerun()


def render_learning_path(path_manager, profile_manager, student_id):
    """Render learning path with all 10 concepts for the selected level"""
    st.title("🛤️ Your Learning Path")
    
    # Get concepts for current subject and level
    subject = st.session_state.selected_subject
    level = st.session_state.student_level
    
    if not subject or not level:
        st.warning("⚠️ Please complete the assessment first to see your learning path.")
        return
    
    # Get the curriculum concepts for this subject and level
    from src.curriculum import Curriculum
    
    curriculum_data = None
    if subject == "Mathematics":
        curriculum_data = Curriculum.MATHEMATICS.get(level.lower())
    elif subject == "Physics":
        curriculum_data = Curriculum.PHYSICS.get(level.lower())
    elif subject == "Chemistry":
        curriculum_data = Curriculum.CHEMISTRY.get(level.lower())
    
    if not curriculum_data:
        st.error(f"❌ No curriculum found for {subject} at {level} level.")
        return
    
    # Update session concepts list
    if not st.session_state.concepts_list:
        st.session_state.concepts_list = curriculum_data
    
    # Initialize completion status if empty
    if not st.session_state.concept_completion_status:
        st.session_state.concept_completion_status = {topic.id: False for topic in curriculum_data}
    
    # Display learning path overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Subject", subject)
    with col2:
        st.metric("📊 Level", level)
    with col3:
        completed = sum(1 for v in st.session_state.concept_completion_status.values() if v)
        st.metric("✅ Completed", f"{completed}/{len(curriculum_data)}")
    
    st.markdown("---")
    
    # Display all 10 concepts as selectable items
    st.subheader("📖 Your Concepts (10 Topics)")
    st.markdown("Click on any concept to start learning or continue where you left off")
    
    # Create a grid/list of concepts
    for idx, topic in enumerate(curriculum_data, 1):
        col1, col2, col3 = st.columns([3, 1, 1])
        
        is_completed = st.session_state.concept_completion_status.get(topic.id, False)
        is_current = len(st.session_state.concepts_list) > 0 and topic.id == st.session_state.concepts_list[st.session_state.current_concept_idx].id
        topic_index = idx - 1  # 0-based index
        current_index = st.session_state.current_concept_idx
        
        # Determine status icon
        if is_current:
            status_icon = "▶️"
            status_text = "Current"
        elif is_completed:
            status_icon = "✅"
            status_text = "Completed"
        else:
            status_icon = "⭕"
            status_text = "Locked"
        
        with col1:
            display_text = f"{status_icon} [**{idx}**] {topic.name}"
            st.write(display_text)
        
        with col2:
            st.write(f"*{topic.level.capitalize()}*")
        
        with col3:
            # Determine button text and behaviour based on status
            if is_current:
                # Current topic - show Resume button
                if st.button(f"▶️ Resume", use_container_width=True, key=f"concept_btn_{topic.id}"):
                    concept_index = topic_index
                    st.session_state.current_concept_idx = concept_index
                    st.session_state.structured_learning_session = {
                        'topic': topic,
                        'concept_index': concept_index,
                        'started_at': str(pd.Timestamp.now())
                    }
                    st.session_state.current_topic_step = "explanation"
                    st.session_state.learning_path_displayed = True
                    st.rerun()
            
            elif is_completed:
                # Completed topic - show Review button
                if st.button(f"📖 Review", use_container_width=True, key=f"concept_btn_{topic.id}"):
                    concept_index = topic_index
                    st.session_state.current_concept_idx = concept_index
                    st.session_state.structured_learning_session = {
                        'topic': topic,
                        'concept_index': concept_index,
                        'started_at': str(pd.Timestamp.now())
                    }
                    st.session_state.current_topic_step = "explanation"
                    st.session_state.learning_path_displayed = True
                    st.rerun()
            
            elif topic_index == current_index + 1:
                # Next topic - show unlock message
                st.button(f"🔒 Finish topic {current_index + 1}", use_container_width=True, disabled=True, key=f"concept_btn_{topic.id}")
            
            else:
                # Topics further ahead - show unlock message
                # All future topics show same unlock requirement: finish current topic
                st.button(f"🔒 Finish topic {current_index + 1}", use_container_width=True, disabled=True, key=f"concept_btn_{topic.id}")
    
    st.markdown("---")
    
    # Progress summary
    st.subheader("📈 Progress Summary")
    concepts_completed = sum(1 for v in st.session_state.concept_completion_status.values() if v)
    concepts_total = len(curriculum_data)
    progress_pct = (concepts_completed / concepts_total * 100) if concepts_total > 0 else 0
    
    st.progress(concepts_completed / concepts_total, text=f"Overall Progress: {progress_pct:.0f}%")
    st.write(f"**{concepts_completed} of {concepts_total}** concepts completed")
    
    st.markdown("---")
    
    # Navigation back to dashboard
    if st.button("📊 Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "Dashboard"
        st.rerun()


def render_analytics(profile_manager, student_id):
    """Render student analytics with real-time data"""
    st.title("📈 Student Analytics")
    
    profile = profile_manager.get_or_create_profile(student_id)
    knowledge = profile.get_knowledge_state_vector()
    
    # Overview
    st.subheader("📊 Student Profile Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Questions", int(profile.overall_metrics['total_questions']))
        st.metric("Correct Answers", int(profile.overall_metrics['total_correct']))
    
    with col2:
        st.metric("Overall Accuracy", f"{profile.overall_metrics['average_accuracy']:.1%}")
        st.metric("Avg Mastery", f"{np.mean(list(knowledge.values())):.1%}")
    
    with col3:
        time_hours = profile.overall_metrics['total_time_spent'] / 3600
        st.metric("Time Invested", f"{time_hours:.1f} hours")
    
    st.markdown("---")
    
    # Learning Progress from actual quiz responses
    st.subheader("📈 Your Learning Progress")
    
    if st.session_state.quiz_responses:
        # Create progress data from actual quiz responses
        quiz_data = []
        cumulative_correct = 0
        for idx, response in enumerate(st.session_state.quiz_responses, 1):
            cumulative_correct += response['correct']
            accuracy = (cumulative_correct / idx) * 100
            quiz_data.append({
                'Question': idx,
                'Accuracy': accuracy,
                'Status': 'Correct' if response['correct'] else 'Incorrect',
                'Concept': response['concept'],
                'Difficulty': response['difficulty']
            })
        
        progress_df = pd.DataFrame(quiz_data)
        
        # Line chart for cumulative accuracy
        fig = px.line(progress_df, x='Question', y='Accuracy',
                      title='Your Cumulative Accuracy Over Time',
                      markers=True,
                      color_discrete_sequence=['#2E86AB'])
        fig.update_layout(yaxis_title="Accuracy (%)", xaxis_title="Question Number")
        st.plotly_chart(fig, use_container_width=True)
        
        # Show quiz statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            total_quiz_q = len(st.session_state.quiz_responses)
            st.metric("Quiz Questions Answered", total_quiz_q)
        
        with col2:
            quiz_correct = sum(1 for r in st.session_state.quiz_responses if r['correct'])
            st.metric("Correct Answers", quiz_correct)
        
        with col3:
            quiz_accuracy = (quiz_correct / total_quiz_q * 100) if total_quiz_q > 0 else 0
            st.metric("Quiz Accuracy", f"{quiz_accuracy:.1f}%")
        
        st.markdown("---")
        
        # Concept-wise performance
        st.subheader("📚 Performance by Topic")
        concept_stats = []
        for concept in set([r['concept'] for r in st.session_state.quiz_responses]):
            concept_responses = [r for r in st.session_state.quiz_responses if r['concept'] == concept]
            correct = sum(1 for r in concept_responses if r['correct'])
            total = len(concept_responses)
            accuracy = (correct / total * 100) if total > 0 else 0
            concept_stats.append({
                'Topic': concept,
                'Questions': total,
                'Correct': correct,
                'Accuracy': f"{accuracy:.1f}%"
            })
        
        if concept_stats:
            concept_df = pd.DataFrame(concept_stats)
            st.dataframe(concept_df, use_container_width=True)
    
    else:
        st.info("📝 No quiz responses yet. Start taking quizzes to see your learning progress!")
    
    st.markdown("---")
    
    # Concept mastery heatmap (from learning sessions)
    st.subheader("🎯 Concept Mastery Status")
    
    concepts = list(knowledge.keys())
    masteries = [knowledge[c] for c in concepts]
    
    fig = go.Figure(data=go.Heatmap(
        z=[masteries],
        x=concepts,
        colorscale='RdYlGn',
        zmin=0,
        zmax=1,
        text=[[f"{m:.0%}" for m in masteries]],
        texttemplate="%{text}",
        showscale=True,
        colorbar=dict(title="Mastery")
    ))
    fig.update_layout(height=150)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Learning path progress
    st.subheader("🛤️ Learning Path Progress")
    
    concepts_completed = sum(1 for v in st.session_state.concept_completion_status.values() if v)
    concepts_total = len(st.session_state.concepts_list) if st.session_state.concepts_list else 10
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Topics Completed", concepts_completed)
    with col2:
        st.metric("Current Topic", st.session_state.current_concept_idx + 1)
    with col3:
        progress_pct = (concepts_completed / concepts_total * 100) if concepts_total > 0 else 0
        st.metric("Completion", f"{progress_pct:.0f}%")
    
    # Progress bar
    st.progress(concepts_completed / concepts_total if concepts_total > 0 else 0, 
                text=f"Learning Path: {concepts_completed}/{concepts_total}")
    
    st.markdown("---")
    
    if st.button("📊 Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "Dashboard"
        st.rerun()


def render_system_info():
    """Render learning overview"""
    st.title("📊 Learning Overview")
    
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
    
    st.subheader("📊 Current Session Information")
    
    # Display current student and session info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Student Name", st.session_state.student_name or "N/A")
        st.metric("Student ID", st.session_state.student_id)
    
    with col2:
        st.metric("Selected Subject", st.session_state.selected_subject or "N/A")
        st.metric("Student Level", st.session_state.student_level or "N/A")
    
    with col3:
        st.metric("Assessment Complete", "✅ Yes" if st.session_state.assessment_complete else "❌ No")
        quiz_count = len(st.session_state.quiz_responses) if st.session_state.quiz_responses else 0
        st.metric("Quizzes Taken", quiz_count)
    
    st.markdown("---")
    
    st.subheader("📈 Learning Position")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        current_topic_num = st.session_state.current_concept_idx + 1 if st.session_state.concepts_list else 0
        st.metric("Current Topic #", current_topic_num)
        if st.session_state.concepts_list and st.session_state.current_concept_idx < len(st.session_state.concepts_list):
            current_topic = st.session_state.concepts_list[st.session_state.current_concept_idx]
            st.write(f"📚 {current_topic.name}")
    
    with col2:
        topics_completed = sum(1 for v in st.session_state.concept_completion_status.values() if v) if st.session_state.concept_completion_status else 0
        total_topics = len(st.session_state.concepts_list) if st.session_state.concepts_list else 10
        st.metric("Topics Completed", f"{topics_completed}/{total_topics}")
    
    with col3:
        progress_pct = (topics_completed / total_topics * 100) if total_topics > 0 else 0
        st.metric("Completion %", f"{progress_pct:.0f}%")
    
    st.markdown("---")
    
    st.subheader("🎯 Quiz Statistics")
    
    if st.session_state.quiz_responses:
        col1, col2, col3 = st.columns(3)
        
        total_quiz_q = len(st.session_state.quiz_responses)
        correct_q = sum(1 for r in st.session_state.quiz_responses if r['correct'])
        quiz_acc = (correct_q / total_quiz_q * 100) if total_quiz_q > 0 else 0
        
        with col1:
            st.metric("Questions Answered", total_quiz_q)
        with col2:
            st.metric("Correct Answers", correct_q)
        with col3:
            st.metric("Quiz Accuracy", f"{quiz_acc:.1f}%")
        
        # Quiz topics covered
        st.markdown("**Topics in Quizzes:**")
        quiz_topics = set([r['concept'] for r in st.session_state.quiz_responses])
        st.write(", ".join(quiz_topics) if quiz_topics else "No quizzes taken yet")
    else:
        st.info("📝 No quizzes taken yet in this session")
    
    st.markdown("---")
    
    st.subheader("💾 Assessment Results")
    
    if st.session_state.assessment_responses:
        assessment_df = pd.DataFrame({
            'Question #': range(1, len(st.session_state.assessment_responses) + 1),
            'Difficulty': [r['difficulty'] for r in st.session_state.assessment_responses],
            'Status': ['✅ Correct' if r['correct'] else '❌ Incorrect' for r in st.session_state.assessment_responses]
        })
        st.dataframe(assessment_df, use_container_width=True)
    else:
        st.info("No assessment data available yet")
    
    st.markdown("---")
    
    if st.button("📊 Back to Dashboard", use_container_width=True):
        st.session_state.current_page = "Dashboard"
        st.rerun()


def render_course_selection():
    """Render course selection page"""
    st.title("Select a Learning Course")

    # Fetch available courses
    courses = CourseManager.get_courses()
    course_options = [(course.id, course.name) for course in courses]

    # Display course selection dropdown
    selected_course_id = st.selectbox(
        "Choose a course:",
        options=[course[0] for course in course_options],
        format_func=lambda course_id: dict(course_options).get(course_id, "Unknown Course")
    )

    # Display course details
    if selected_course_id:
        selected_course = CourseManager.get_course(selected_course_id)
        st.subheader(selected_course.name)
        st.write(selected_course.description)
        st.write(f"**Difficulty:** {selected_course.difficulty.capitalize()}")
        st.write(f"**Duration:** {selected_course.duration_hours} hours")
        st.write(f"**Concepts Covered:** {', '.join(selected_course.concepts)}")

        # Confirm course selection
        if st.button("Start Course", use_container_width=True, type="primary"):
            st.session_state.selected_course = selected_course_id
            st.success(f"✅ Course selected: {selected_course.name}")
            st.info("📚 Get ready for your assessment!")
            st.rerun()
            st.success(f"You have selected the course: {selected_course.name}")


def main():
    """Main Streamlit app"""
    
    # Initialize session
    session_manager = TutorSessionManager()
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        render_login_page()
        return
    
    # Check if subject is selected
    if not st.session_state.selected_subject:
        render_subject_selection()
        return
    
    # Initialize managers
    concepts = ['algebra', 'geometry', 'trigonometry', 'calculus', 'statistics']
    
    profile_manager = LearnerProfileManager(concepts)
    
    dkt = SimplifiedDKT(concepts)
    
    path_manager = AdaptivePathManager(
        LearningPathGenerator(concepts)
    )
    
    tutor_agent = PersonalizedTutorAgent()
    
    # Auto-assign course based on selected subject if not already selected
    if not st.session_state.selected_course and st.session_state.selected_subject:
        # Map subject to course
        subject_to_course = {
            "Mathematics": "math-101",
            "Physics": "math-201",
            "Chemistry": "math-301"
        }
        assigned_course = subject_to_course.get(st.session_state.selected_subject, "math-101")
        st.session_state.selected_course = assigned_course
    
    # Check if initial assessment is complete
    if not st.session_state.assessment_complete:
        render_initial_assessment(tutor_agent, profile_manager, st.session_state.student_id)
        return
    
    # If structured learning flow should be displayed (after assessment)
    if st.session_state.learning_path_displayed:
        render_structured_learning_flow()
        return
    
    # If old learning path should be displayed (fallback)
    # if st.session_state.learning_path_displayed:
    #     render_learning_path_post_assessment()
    #     return
    
    # Render sidebar (only after login and assessment)
    sidebar_page = render_sidebar()
    
    # Initialize last sidebar page if not already done
    if 'last_sidebar_page' not in st.session_state:
        st.session_state.last_sidebar_page = sidebar_page
    
    # If sidebar selection changed, reset current_page so sidebar takes precedence
    if sidebar_page != st.session_state.last_sidebar_page:
        st.session_state.current_page = None
    st.session_state.last_sidebar_page = sidebar_page
    
    # Determine which page to display
    # Priority: current_page (from buttons) > sidebar selection
    page = sidebar_page
    
    # If a button set current_page, use it
    if st.session_state.current_page:
        page = st.session_state.current_page
    
    # Route pages
    if page == "Dashboard":
        render_dashboard_post_assessment()
    
    elif page == "Interactive Quiz":
        render_quiz(st.session_state.student_id, profile_manager, tutor_agent)
    
    elif page == "Learning Path":
        render_learning_path(path_manager, profile_manager, st.session_state.student_id)
    
    elif page == "Student Analytics":
        render_analytics(profile_manager, st.session_state.student_id)
    
    elif page == "Learning Overview":
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
