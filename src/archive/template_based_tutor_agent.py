"""
ARCHIVED: Template-Based Tutor Agent
This file contains the original hardcoded template-based feedback system.
Archived on: 2026-01-30
Purpose: Kept for future fallback integration

DO NOT USE - Currently using Groq AI instead
Re-integration instructions in: ../../TODO_TEMPLATE_INTEGRATION.md
"""

from typing import Dict, List
import random


class TutorFeedbackGenerator:
    """ARCHIVED: Template-based feedback generator (DO NOT USE)"""
    
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
        """Generate immediate feedback - ARCHIVED"""
        feedback = ""
        
        if is_correct:
            accuracy_level = 'excellent' if difficulty == 'Hard' else 'good'
            feedback = random.choice(self.encouragement_phrases[accuracy_level])
        else:
            feedback = "Not quite right, but let's learn from this."
            if difficulty == 'Hard':
                feedback += " This is a challenging question!"
        
        if time_spent > estimated_time * 1.5:
            feedback += f"\n💡 You spent {int(time_spent / 60)} min on this - consider a different approach or review the concept."
        elif time_spent < estimated_time * 0.4:
            feedback += "\n⚡ That was fast! Make sure you've understood the concept fully."
        
        return feedback
    
    def generate_hint(self, concept: str, hint_level: int = 1,
                     attempt_number: int = 1) -> str:
        """Generate progressive hints - ARCHIVED"""
        hints = self.hint_database.get(concept, self.hint_database['default'])
        hint_idx = min(hint_level - 1, len(hints) - 1)
        selected_hint = hints[hint_idx]
        return f"💭 Hint {hint_level}: {selected_hint}"
    
    def generate_concept_explanation(self, concept: str, 
                                    detail_level: str = 'basic') -> str:
        """Generate explanation - ARCHIVED"""
        base = self.concept_explanations.get(concept, self.concept_explanations['default'])
        
        if detail_level == 'basic':
            return base
        elif detail_level == 'intermediate':
            return base + "\n\nKey points to remember:\n• First, understand the fundamentals.\n• Then, apply to problems.\n• Finally, explain to others."
        else:
            return base + "\n\nAdvanced insights:\n• This concept connects to related areas.\n• Real-world applications include...\n• Common misconceptions to avoid..."


# Archive metadata
ARCHIVE_INFO = {
    'original_filename': 'tutor_agent.py',
    'archived_date': '2026-01-30',
    'reason': 'Archived to use Groq AI instead of hardcoded templates',
    'total_lines': 674,
    'hardcoded_strings': 50,
    'static_dictionaries': 4,
    'classes_archived': ['TutorFeedbackGenerator', 'ConversationalTutor'],
    're_integration_guide': '../../TODO_TEMPLATE_INTEGRATION.md'
}
