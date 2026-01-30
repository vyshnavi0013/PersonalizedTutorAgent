"""
Tutor Agent with Groq AI-Powered Feedback (AI-ONLY MODE)
Provides personalized feedback, hints, and encouragement using Groq AI
Template-based code archived to: src/archive/template_based_tutor_agent.py
"""

from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TutorFeedbackGenerator:
    """Generates personalized feedback based on performance"""
    
    def __init__(self):
        """Initialize tutor with feedback templates"""
        
        self.concept_explanations = {
            'Concept_1': 'This concept focuses on foundational principles...',
            'Concept_2': 'This concept builds on earlier knowledge...',
            'Concept_3': 'This is an advanced concept requiring practice...',
            'default': 'Let\'s focus on understanding this concept step by step.'
        }
        
        self.hint_database = {
            'Concept_1': [
                'Start by reading the definition carefully.',
                'Try drawing a diagram or visual representation.',
                'Look for examples in your study material.',
                'Apply the concept to a simple real-world scenario.'
            ],
            'Concept_2': [
                'Review the prerequisite concept first.',
                'Identify the key steps in solving this problem.',
                'Work through an example solution.',
                'Try a similar problem with different numbers.'
            ],
            'default': [
                'Read the question carefully and identify what\'s being asked.',
                'Break the problem into smaller parts.',
                'Check your understanding with an example.',
                'Review the relevant concept material.'
            ]
        }
        
        self.motivational_phrases = [
            'Great effort! Keep practicing.',
            'You\'re making progress! Don\'t give up.',
            'Nice try! Let\'s learn from this.',
            'Every mistake is a learning opportunity.',
            'Your persistence will pay off!',
            'You\'re getting closer to mastery!',
            'Practice makes perfect!',
            'Don\'t worry, this is challenging for many!'
        ]
        
        self.encouragement_phrases = {
            'excellent': [
                'Excellent work! You\'ve mastered this concept.',
                'Outstanding! You clearly understand this well.',
                'Perfect! You\'re progressing rapidly!',
                'Superb! Keep up this excellent work!'
            ],
            'good': [
                'Good job! You\'re on the right track.',
                'Nice! You\'re making solid progress.',
                'Well done! Keep practicing to master it.',
                'Impressive! You\'re learning quickly.'
            ],
            'needs_improvement': [
                'Let\'s work on this together.',
                'Don\'t worry, it gets easier with practice.',
                'This is a challenging concept; keep trying!',
                'You\'ll get there with more practice.'
            ]
        }
    
    def generate_immediate_feedback(self, is_correct: bool, 
                                   concept: str, difficulty: str,
                                   time_spent: int,
                                   estimated_time: int) -> str:
        """
        Generate immediate feedback after quiz response
        
        Args:
            is_correct: Whether answer was correct
            concept: Concept tested
            difficulty: Question difficulty
            time_spent: Time spent on question
            estimated_time: Expected time for question
            
        Returns:
            Immediate feedback message
        """
        feedback = ""
        
        if is_correct:
            # Correct answer feedback
            accuracy_level = 'excellent' if difficulty == 'Hard' else 'good'
            feedback = random.choice(self.encouragement_phrases[accuracy_level])
        else:
            # Incorrect answer feedback
            feedback = "Not quite right, but let's learn from this."
            if difficulty == 'Hard':
                feedback += " This is a challenging question!"
        
        # Add time-based feedback
        if time_spent > estimated_time * 1.5:
            feedback += f"\n💡 You spent {int(time_spent / 60)} min on this - consider a different approach or review the concept."
        elif time_spent < estimated_time * 0.4:
            feedback += "\n⚡ That was fast! Make sure you've understood the concept fully."
        
        return feedback
    
    def generate_hint(self, concept: str, hint_level: int = 1,
                     attempt_number: int = 1) -> str:
        """
        Generate progressive hints for learner
        
        Args:
            concept: Target concept
            hint_level: Level of hint detail (1=minimal, 3=detailed)
            attempt_number: Which attempt is this
            
        Returns:
            Hint text
        """
        hints = self.hint_database.get(concept, self.hint_database['default'])
        
        # Provide progressively detailed hints
        hint_idx = min(hint_level - 1, len(hints) - 1)
        selected_hint = hints[hint_idx]
        
        return f"💭 Hint {hint_level}: {selected_hint}"
    
    def generate_concept_explanation(self, concept: str, 
                                    detail_level: str = 'basic') -> str:
        """
        Generate explanation for a concept
        
        Args:
            concept: Target concept
            detail_level: 'basic', 'intermediate', or 'advanced'
            
        Returns:
            Concept explanation
        """
        base = self.concept_explanations.get(concept, self.concept_explanations['default'])
        
        if detail_level == 'basic':
            return base
        elif detail_level == 'intermediate':
            return base + "\n\nKey points to remember:\n• First, understand the fundamentals.\n• Then, apply to problems.\n• Finally, explain to others."
        else:  # advanced
            return base + "\n\nAdvanced insights:\n• This concept connects to related areas.\n• Real-world applications include...\n• Common misconceptions to avoid..."
    
    def generate_error_analysis(self, concept: str, common_mistakes: List[str],
                               mastery_level: float) -> str:
        """
        Generate analysis of common errors
        
        Args:
            concept: Target concept
            common_mistakes: List of common mistakes for this concept
            mastery_level: Current mastery level (0-1)
            
        Returns:
            Error analysis message
        """
        analysis = f"📊 Error Analysis for {concept}:\n"
        analysis += f"Current Mastery Level: {mastery_level:.1%}\n\n"
        
        if mastery_level < 0.4:
            analysis += "🎯 Focus Area: You're still building foundational knowledge.\n"
            analysis += "Recommendation: Review basic concepts and practice simpler problems.\n"
        elif mastery_level < 0.7:
            analysis += "🎯 Focus Area: You're progressing well but need more practice.\n"
            analysis += "Recommendation: Practice with more complex problems.\n"
        else:
            analysis += "🎯 Focus Area: You're approaching mastery!\n"
            analysis += "Recommendation: Teach others or work on advanced applications.\n"
        
        if common_mistakes:
            analysis += "\nCommon Mistakes to Avoid:\n"
            for i, mistake in enumerate(common_mistakes[:3], 1):
                analysis += f"  {i}. {mistake}\n"
        
        return analysis
    
    def generate_next_steps(self, concept: str, mastery_level: float,
                           weak_concepts: List[str],
                           available_concepts: List[str]) -> str:
        """
        Generate personalized next steps
        
        Args:
            concept: Current concept
            mastery_level: Current mastery (0-1)
            weak_concepts: List of weak concepts
            available_concepts: Available next concepts
            
        Returns:
            Next steps recommendation
        """
        recommendation = "📚 Your Personalized Learning Path:\n\n"
        
        if mastery_level < 0.6:
            recommendation += f"1. Continue practicing {concept}\n"
            recommendation += "   - Complete 5 more practice questions\n"
            recommendation += "   - Review the concept explanation\n"
            recommendation += "   - Watch tutorial if available\n"
        else:
            recommendation += f"1. {concept} - Ready for advanced problems\n"
            recommendation += "   - Try harder difficulty questions\n"
            recommendation += "   - Apply to real-world scenarios\n\n"
            
            # Suggest next concept
            if available_concepts:
                next_concept = available_concepts[0]
                recommendation += f"2. Move on to {next_concept}\n"
                recommendation += f"   - This builds on {concept}\n"
                recommendation += "   - Start with easier problems\n"
        
        # Address weak areas
        if weak_concepts:
            recommendation += f"\n3. Review weak areas:\n"
            for wc in weak_concepts[:2]:
                recommendation += f"   - {wc}: Set 15-minute review session\n"
        
        return recommendation
    
    def generate_motivational_message(self, mastery_level: float,
                                     total_questions: int,
                                     accuracy: float,
                                     streak: int = 0) -> str:
        """
        Generate motivational message based on progress
        
        Args:
            mastery_level: Current overall mastery
            total_questions: Total questions attempted
            accuracy: Overall accuracy
            streak: Correct answer streak
            
        Returns:
            Motivational message
        """
        message = random.choice(self.motivational_phrases) + "\n\n"
        
        # Add progress metrics
        message += f"📈 Your Progress:\n"
        message += f"  • Mastery Level: {mastery_level:.1%}\n"
        message += f"  • Questions Completed: {total_questions}\n"
        message += f"  • Accuracy: {accuracy:.1%}\n"
        
        if streak > 2:
            message += f"  • 🔥 Current Streak: {streak} correct answers!\n"
        
        # Add milestone messages
        if total_questions == 10:
            message += "\n🎯 Milestone: You've completed 10 questions! Keep going!\n"
        elif total_questions == 25:
            message += "\n🏆 Milestone: 25 questions done! You're becoming an expert!\n"
        elif total_questions == 50:
            message += "\n⭐ Milestone: 50 questions! You've shown real dedication!\n"
        
        return message


class ConversationalTutor:
    """Conversational interface for tutor"""
    
    def __init__(self, feedback_generator: TutorFeedbackGenerator):
        """
        Initialize conversational tutor
        
        Args:
            feedback_generator: TutorFeedbackGenerator instance
        """
        self.feedback_gen = feedback_generator
        self.conversation_history: List[Dict[str, str]] = []
        self.hint_count: Dict[str, int] = {}
    
    def process_student_input(self, student_message: str, 
                            context: Dict) -> str:
        """
        Process student message and generate tutor response
        
        Args:
            student_message: Message from student
            context: Context dict with concept, mastery, etc.
            
        Returns:
            Tutor response
        """
        # Simple intent detection
        if 'hint' in student_message.lower():
            concept = context.get('concept', 'default')
            hint_count = self.hint_count.get(concept, 0) + 1
            self.hint_count[concept] = hint_count
            return self.feedback_gen.generate_hint(concept, hint_level=hint_count)
        
        elif 'explain' in student_message.lower():
            concept = context.get('concept', 'default')
            return self.feedback_gen.generate_concept_explanation(
                concept, detail_level='basic'
            )
        
        elif 'help' in student_message.lower() or 'confused' in student_message.lower():
            concept = context.get('concept', 'default')
            return "I understand! Let me help you.\n\n" + \
                   self.feedback_gen.generate_concept_explanation(concept, 'intermediate')
        
        else:
            return "I'm here to help! You can ask for: \n- 'hint' for help\n- 'explain' for concept details\n- 'next steps' for recommendations"
    
    def add_to_conversation(self, role: str, message: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'message': message
        })
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history


class PersonalizedTutorAgent:
    """
    Main tutor agent combining all components
    Integrates AI-powered feedback (Groq) with template-based fallback
    Features: feedback generation, hints, explanations, and guidance
    """
    
    def __init__(self, use_ai: bool = True):
        """
        Initialize personalized tutor agent
        
        Args:
            use_ai: Whether to use Groq AI (True) or template-based feedback (False)
        """
        self.feedback_gen = TutorFeedbackGenerator()
        self.conversational = ConversationalTutor(self.feedback_gen)
        self.use_ai = use_ai
        self.groq_ai = None
        
        # Initialize Groq AI if requested
        if use_ai:
            try:
                from .groq_ai import GroqAITutor
                self.groq_ai = GroqAITutor()
                logger.info("✅ PersonalizedTutorAgent initialized with AI (Groq)")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize Groq AI: {e}")
                logger.warning("📝 Falling back to template-based feedback")
                self.use_ai = False
                self.groq_ai = None
        else:
            logger.info("ℹ️  PersonalizedTutorAgent initialized in template mode")
    
    def generate_immediate_feedback(self,
                                   is_correct: bool,
                                   student_response: str = "",
                                   correct_answer: str = "",
                                   concept: str = "",
                                   difficulty: str = "Medium",
                                   mastery_level: float = 0.5,
                                   time_spent: int = 30,
                                   estimated_time: int = 30) -> str:
        """
        Generate immediate feedback using AI or templates
        
        Args:
            is_correct: Whether answer was correct
            student_response: Student's response
            correct_answer: Correct answer
            concept: Concept being tested
            difficulty: Question difficulty
            mastery_level: Current mastery (0-1)
            time_spent: Time spent on question
            estimated_time: Expected time
            
        Returns:
            Feedback message
        """
        if self.use_ai and self.groq_ai:
            try:
                return self.groq_ai.generate_immediate_feedback(
                    is_correct=is_correct,
                    student_response=student_response,
                    correct_answer=correct_answer,
                    concept=concept,
                    difficulty=difficulty,
                    mastery_level=mastery_level,
                    time_spent=time_spent,
                    estimated_time=estimated_time
                )
            except Exception as e:
                logger.warning(f"⚠️ AI feedback failed: {e}. Using templates.")
                return self.feedback_gen.generate_immediate_feedback(
                    is_correct, concept, difficulty, time_spent, estimated_time
                )
        else:
            # Use template-based feedback
            return self.feedback_gen.generate_immediate_feedback(
                is_correct, concept, difficulty, time_spent, estimated_time
            )
    
    def generate_hint(self,
                     concept: str,
                     question: str = "",
                     student_attempt: str = "",
                     hint_level: int = 1,
                     attempt_number: int = 1) -> str:
        """
        Generate hint using AI or templates
        
        Args:
            concept: Target concept
            question: The quiz question
            student_attempt: Student's attempt
            hint_level: Hint detail level (1-3)
            attempt_number: Which attempt
            
        Returns:
            Hint text
        """
        if self.use_ai and self.groq_ai:
            try:
                return self.groq_ai.generate_hint(
                    concept=concept,
                    question=question,
                    student_attempt=student_attempt,
                    hint_level=hint_level,
                    attempt_number=attempt_number
                )
            except Exception as e:
                logger.warning(f"⚠️ AI hint failed: {e}. Using templates.")
                return self.feedback_gen.generate_hint(concept, hint_level, attempt_number)
        else:
            # Use template-based hints
            return self.feedback_gen.generate_hint(concept, hint_level, attempt_number)
    
    def generate_explanation(self,
                           concept: str,
                           context: Optional[str] = None,
                           detail_level: str = 'basic') -> str:
        """
        Generate concept explanation using AI or templates
        
        Args:
            concept: Concept to explain
            context: Additional context
            detail_level: 'basic', 'intermediate', or 'advanced'
            
        Returns:
            Explanation text
        """
        if self.use_ai and self.groq_ai:
            try:
                return self.groq_ai.generate_explanation(
                    concept=concept,
                    context=context,
                    detail_level=detail_level
                )
            except Exception as e:
                logger.warning(f"⚠️ AI explanation failed: {e}. Using templates.")
                return self.feedback_gen.generate_concept_explanation(concept, detail_level)
        else:
            # Use template-based explanation
            return self.feedback_gen.generate_concept_explanation(concept, detail_level)
    
    def generate_next_steps(self,
                          concept: str,
                          mastery_level: float,
                          weak_areas: List[str],
                          available_concepts: List[str],
                          total_questions: int = 0) -> str:
        """
        Generate personalized next steps using AI or templates
        
        Args:
            concept: Current concept
            mastery_level: Current mastery (0-1)
            weak_areas: List of weak areas
            available_concepts: Available next concepts
            total_questions: Total questions completed
            
        Returns:
            Next steps recommendation
        """
        if self.use_ai and self.groq_ai:
            try:
                return self.groq_ai.generate_next_steps(
                    concept=concept,
                    mastery_level=mastery_level,
                    weak_areas=weak_areas,
                    available_concepts=available_concepts,
                    total_questions=total_questions
                )
            except Exception as e:
                logger.warning(f"⚠️ AI next steps failed: {e}. Using templates.")
                return self.feedback_gen.generate_next_steps(
                    concept, mastery_level, weak_areas, available_concepts
                )
        else:
            # Use template-based next steps
            return self.feedback_gen.generate_next_steps(
                concept, mastery_level, weak_areas, available_concepts
            )
    
    def generate_motivational_message(self,
                                     mastery_level: float,
                                     total_questions: int,
                                     accuracy: float,
                                     streak: int = 0,
                                     recent_performance: Optional[str] = None) -> str:
        """
        Generate motivational message using AI or templates
        
        Args:
            mastery_level: Overall mastery level
            total_questions: Total questions completed
            accuracy: Overall accuracy
            streak: Correct answer streak
            recent_performance: Description of recent performance
            
        Returns:
            Motivational message
        """
        if self.use_ai and self.groq_ai:
            try:
                return self.groq_ai.generate_motivational_message(
                    mastery_level=mastery_level,
                    total_questions=total_questions,
                    accuracy=accuracy,
                    streak=streak,
                    recent_performance=recent_performance
                )
            except Exception as e:
                logger.warning(f"⚠️ AI motivation failed: {e}. Using templates.")
                return self.feedback_gen.generate_motivational_message(
                    mastery_level, total_questions, accuracy, streak
                )
        else:
            # Use template-based motivation
            return self.feedback_gen.generate_motivational_message(
                mastery_level, total_questions, accuracy, streak
            )
    
    def create_quiz_completion_summary(self, quiz_stats: Dict,
                                      concept: str,
                                      learning_path: List[Dict],
                                      weak_concepts: List[str]) -> str:
        """
        Create comprehensive quiz completion summary
        
        Args:
            quiz_stats: Quiz statistics
            concept: Current concept
            learning_path: Upcoming learning path
            weak_concepts: Identified weak concepts
            
        Returns:
            Formatted completion summary
        """
        summary = "\n" + "="*50 + "\n"
        summary += "        QUIZ COMPLETION SUMMARY\n"
        summary += "="*50 + "\n"
        
        # Performance
        summary += f"\n📊 PERFORMANCE:\n"
        summary += f"  Accuracy: {quiz_stats['accuracy']:.1%}\n"
        summary += f"  Questions: {quiz_stats['total_questions']}\n"
        summary += f"  Time: {quiz_stats['avg_time_spent']:.0f}s average\n"
        
        # Feedback
        mastery = 0.5  # Would come from actual KT model
        if quiz_stats['accuracy'] > 0.8:
            summary += f"\n💪 Excellent work! You've mastered {concept}!\n"
        elif quiz_stats['accuracy'] > 0.6:
            summary += f"\n👍 Good progress! Keep practicing {concept}.\n"
        else:
            summary += f"\n📚 Keep learning! More practice needed for {concept}.\n"
        
        # Next steps
        summary += f"\n🎯 NEXT STEPS:\n"
        if learning_path:
            next_concept = learning_path[0].get('concept', 'next topic')
            summary += f"  1. Move on to: {next_concept}\n"
        if weak_concepts:
            summary += f"  2. Review weak concepts:\n"
            for wc in weak_concepts[:2]:
                summary += f"     - {wc}\n"
        summary += f"\n"
        
        return summary
    
    def generate_session_report(self, student_data: Dict) -> str:
        """
        Generate learning session report
        
        Args:
            student_data: Student performance data
            
        Returns:
            Formatted session report
        """
        report = "\n" + "="*50 + "\n"
        report += "      LEARNING SESSION REPORT\n"
        report += "="*50 + "\n"
        
        report += f"\n📅 Session Summary:\n"
        report += f"  Total Questions: {student_data.get('total_questions', 0)}\n"
        report += f"  Overall Accuracy: {student_data.get('accuracy', 0):.1%}\n"
        report += f"  Concepts Covered: {student_data.get('concepts_count', 0)}\n"
        
        report += f"\n🎖️ Achievements:\n"
        if student_data.get('accuracy', 0) > 0.8:
            report += "  ⭐ High Achiever - Excellent Performance!\n"
        if student_data.get('total_questions', 0) >= 10:
            report += "  🏃 Dedicated Learner - Many questions completed!\n"
        
        report += f"\n💡 Recommendations:\n"
        report += f"  - Focus on: {', '.join(student_data.get('weak_concepts', []))}\n"
        report += f"  - Next: {student_data.get('next_concept', 'Continue learning')}\n"
        
        report += "\n" + "="*50 + "\n"
        return report


if __name__ == '__main__':
    # Example usage
    tutor = PersonalizedTutorAgent()
    
    # Generate feedback
    feedback = tutor.feedback_gen.generate_immediate_feedback(
        is_correct=True,
        concept='Concept_1',
        difficulty='Medium',
        time_spent=45,
        estimated_time=30
    )
    print("Immediate Feedback:")
    print(feedback)
    
    # Generate hint
    hint = tutor.feedback_gen.generate_hint('Concept_1', hint_level=1)
    print("\n" + hint)
    
    # Generate motivation
    motivation = tutor.feedback_gen.generate_motivational_message(
        mastery_level=0.65,
        total_questions=10,
        accuracy=0.7,
        streak=3
    )
    print("\n" + motivation)
