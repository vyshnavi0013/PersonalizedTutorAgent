"""
Tutor Agent with Groq AI-Powered Feedback (AI-ONLY MODE)
Provides personalized feedback, hints, and encouragement using Groq AI exclusively
Template-based code archived to: src/archive/template_based_tutor_agent.py
Backup of original file: src/archive/tutor_agent_backup.py
"""

from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PersonalizedTutorAgent:
    """
    Main tutor agent using Groq AI for all feedback
    Features: AI-powered feedback generation, hints, explanations, and guidance
    NO TEMPLATE FALLBACK - Pure AI-first approach
    """
    
    def __init__(self):
        """
        Initialize personalized tutor agent with Groq AI
        
        Raises:
            Exception: If Groq AI initialization fails (no fallback)
        """
        # Initialize Groq AI (required - no fallback)
        try:
            from src.groq_ai import GroqAITutor
            self.groq_ai = GroqAITutor()
            logger.info("✅ PersonalizedTutorAgent initialized with Groq AI (AI-ONLY MODE)")
        except Exception as e:
            logger.error(f"❌ FATAL: Failed to initialize Groq AI: {e}")
            logger.error("Cannot proceed without AI - please check configuration")
            logger.error("Settings file: settings.json")
            logger.error("Required: Groq API key configured")
            raise
    
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
        Generate immediate feedback using Groq AI
        
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
            AI-generated feedback message
        """
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
    
    def generate_hint(self,
                     concept: str,
                     question: str = "",
                     student_attempt: str = "",
                     hint_level: int = 1,
                     attempt_number: int = 1) -> str:
        """
        Generate hint using Groq AI
        
        Args:
            concept: Target concept
            question: The quiz question
            student_attempt: Student's attempt
            hint_level: Hint detail level (1-3)
            attempt_number: Which attempt
            
        Returns:
            AI-generated hint text
        """
        return self.groq_ai.generate_hint(
            concept=concept,
            question=question,
            student_attempt=student_attempt,
            hint_level=hint_level,
            attempt_number=attempt_number
        )
    
    def generate_explanation(self,
                           concept: str,
                           context: Optional[str] = None,
                           detail_level: str = 'basic') -> str:
        """
        Generate concept explanation using Groq AI
        
        Args:
            concept: Concept to explain
            context: Additional context
            detail_level: 'basic', 'intermediate', or 'advanced'
            
        Returns:
            AI-generated explanation text
        """
        return self.groq_ai.generate_explanation(
            concept=concept,
            context=context,
            detail_level=detail_level
        )
    
    def generate_next_steps(self,
                          concept: str,
                          mastery_level: float,
                          weak_areas: List[str],
                          available_concepts: List[str],
                          total_questions: int = 0) -> str:
        """
        Generate personalized next steps using Groq AI
        
        Args:
            concept: Current concept
            mastery_level: Current mastery (0-1)
            weak_areas: List of weak areas
            available_concepts: Available next concepts
            total_questions: Total questions completed
            
        Returns:
            AI-generated next steps recommendation
        """
        return self.groq_ai.generate_next_steps(
            concept=concept,
            mastery_level=mastery_level,
            weak_areas=weak_areas,
            available_concepts=available_concepts,
            total_questions=total_questions
        )
    
    def generate_motivational_message(self,
                                     mastery_level: float,
                                     total_questions: int,
                                     accuracy: float,
                                     streak: int = 0,
                                     recent_performance: Optional[str] = None) -> str:
        """
        Generate motivational message using Groq AI
        
        Args:
            mastery_level: Overall mastery level
            total_questions: Total questions completed
            accuracy: Overall accuracy
            streak: Correct answer streak
            recent_performance: Description of recent performance
            
        Returns:
            AI-generated motivational message
        """
        return self.groq_ai.generate_motivational_message(
            mastery_level=mastery_level,
            total_questions=total_questions,
            accuracy=accuracy,
            streak=streak,
            recent_performance=recent_performance
        )
    
    def analyze_error_pattern(self,
                            concept: str,
                            errors: List[str],
                            mastery_level: float) -> str:
        """
        Analyze error patterns using Groq AI
        
        Args:
            concept: Concept where errors occurred
            errors: List of common errors
            mastery_level: Current mastery level
            
        Returns:
            AI-generated error pattern analysis
        """
        return self.groq_ai.analyze_error_pattern(
            concept=concept,
            errors=errors,
            mastery_level=mastery_level
        )
    
    def create_quiz_completion_summary(self, quiz_stats: Dict,
                                      concept: str,
                                      learning_path: List[Dict],
                                      weak_concepts: List[str]) -> str:
        """
        Create comprehensive quiz completion summary using AI
        
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
        
        # AI Feedback
        try:
            mastery_feedback = self.generate_motivational_message(
                mastery_level=quiz_stats['accuracy'],
                total_questions=quiz_stats['total_questions'],
                accuracy=quiz_stats['accuracy']
            )
            summary += f"\n💬 AI FEEDBACK:\n{mastery_feedback}\n"
        except Exception as e:
            logger.error(f"Error generating AI feedback: {e}")
            summary += f"\n⚠️ Unable to generate AI feedback at this moment.\n"
        
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
    
    def generate_quiz_question(self,
                             concept: str,
                             difficulty: str = "Medium",
                             mastery_level: float = 0.5) -> Dict:
        """
        Generate an AI-created quiz question with correct answer
        
        Args:
            concept: Concept to create question for
            difficulty: Easy/Medium/Hard
            mastery_level: Student's current mastery level (0-1)
            
        Returns:
            Dict with question, options, correct_answer, explanation
        """
        return self.groq_ai.generate_quiz_question(concept, difficulty, mastery_level)
    
    def generate_session_report(self, student_data: Dict) -> str:
        """
        Generate learning session report using AI insights
        
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
    # Example usage - AI-ONLY mode (no templates)
    try:
        tutor = PersonalizedTutorAgent()
        
        # Generate feedback
        feedback = tutor.generate_immediate_feedback(
            is_correct=True,
            concept='Mathematics',
            difficulty='Medium',
            time_spent=45,
            estimated_time=30
        )
        print("AI Feedback:")
        print(feedback)
        print("\n" + "-"*50 + "\n")
        
        # Generate hint
        hint = tutor.generate_hint('Mathematics', hint_level=1)
        print("AI Hint:")
        print(hint)
        print("\n" + "-"*50 + "\n")
        
        # Generate motivation
        motivation = tutor.generate_motivational_message(
            mastery_level=0.65,
            total_questions=10,
            accuracy=0.7,
            streak=3
        )
        print("AI Motivation:")
        print(motivation)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check settings.json for Groq API key")
        print("2. Ensure .env file has GROQ_API_KEY if using environment variable")
        print("3. Verify API key is valid and has access")
        print("4. Check internet connection for Groq API access")
