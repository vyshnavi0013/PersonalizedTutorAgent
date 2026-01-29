"""
Adaptive Quiz Engine
Dynamically generates and adapts quiz difficulty based on student performance
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import random


class Question:
    """Represents a quiz question"""
    
    def __init__(self, question_id: int, concept: str, difficulty: str,
                 bloom_level: str = 'Understand', estimated_time: int = 30):
        """
        Initialize question
        
        Args:
            question_id: Unique question identifier
            concept: Concept being tested
            difficulty: Easy/Medium/Hard
            bloom_level: Bloom's taxonomy level
            estimated_time: Expected time to solve (seconds)
        """
        self.question_id = question_id
        self.concept = concept
        self.difficulty = difficulty
        self.bloom_level = bloom_level
        self.estimated_time = estimated_time
        
        # Performance statistics
        self.attempts = 0
        self.correct = 0
        self.total_time = 0
        self.discrimination_index = 0.0
        
    def get_difficulty_score(self) -> float:
        """Get numeric difficulty score"""
        difficulty_map = {'Easy': 1, 'Medium': 2, 'Hard': 3}
        return difficulty_map.get(self.difficulty, 2)
    
    def update_statistics(self, correct: int, time_spent: int):
        """Update question statistics"""
        self.attempts += 1
        self.correct += correct
        self.total_time += time_spent
    
    def get_difficulty_index(self) -> float:
        """
        Get question difficulty index (% of students getting it wrong)
        
        Returns:
            Difficulty index (0-1, where 1 is hardest)
        """
        if self.attempts == 0:
            return 0.5
        return 1 - (self.correct / self.attempts)


class QuestionBank:
    """Manages the question bank"""
    
    def __init__(self, questions_df: pd.DataFrame):
        """
        Initialize question bank from dataframe
        
        Args:
            questions_df: DataFrame with columns:
                question_id, concept, difficulty, bloom_level, avg_solve_time
        """
        self.questions: Dict[int, Question] = {}
        
        for _, row in questions_df.iterrows():
            q = Question(
                question_id=row['question_id'],
                concept=row['concept'],
                difficulty=row['difficulty'],
                bloom_level=row.get('bloom_level', 'Understand'),
                estimated_time=int(row.get('avg_solve_time', 30))
            )
            self.questions[q.question_id] = q
    
    def get_questions_by_concept(self, concept: str,
                                difficulty: str = None) -> List[Question]:
        """
        Get questions for a concept
        
        Args:
            concept: Target concept
            difficulty: Optional difficulty filter
            
        Returns:
            List of matching questions
        """
        matching = [q for q in self.questions.values() if q.concept == concept]
        
        if difficulty:
            matching = [q for q in matching if q.difficulty == difficulty]
        
        return matching
    
    def get_question_by_id(self, question_id: int) -> Optional[Question]:
        """Get specific question by ID"""
        return self.questions.get(question_id)
    
    def update_question_statistics(self, question_id: int, 
                                   correct: int, time_spent: int):
        """Update question statistics after attempt"""
        if question_id in self.questions:
            self.questions[question_id].update_statistics(correct, time_spent)
    
    def get_bank_statistics(self) -> Dict:
        """Get overall bank statistics"""
        if not self.questions:
            return {}
        
        difficulties = {}
        concepts = {}
        
        for q in self.questions.values():
            # By difficulty
            if q.difficulty not in difficulties:
                difficulties[q.difficulty] = {'count': 0, 'avg_difficulty': 0}
            difficulties[q.difficulty]['count'] += 1
            difficulties[q.difficulty]['avg_difficulty'] += q.get_difficulty_index()
            
            # By concept
            if q.concept not in concepts:
                concepts[q.concept] = {'count': 0, 'avg_difficulty': 0}
            concepts[q.concept]['count'] += 1
            concepts[q.concept]['avg_difficulty'] += q.get_difficulty_index()
        
        # Average difficulties
        for d in difficulties.values():
            if d['count'] > 0:
                d['avg_difficulty'] /= d['count']
        for c in concepts.values():
            if c['count'] > 0:
                c['avg_difficulty'] /= c['count']
        
        return {
            'total_questions': len(self.questions),
            'by_difficulty': difficulties,
            'by_concept': concepts
        }


class AdaptiveQuizEngine:
    """
    Generates adaptive quizzes that adjust difficulty based on performance
    Implements item response theory principles for mini-project
    """
    
    def __init__(self, question_bank: QuestionBank,
                 target_accuracy: float = 0.65):
        """
        Initialize quiz engine
        
        Args:
            question_bank: QuestionBank instance
            target_accuracy: Target accuracy to maintain (~65% shows learning)
        """
        self.qbank = question_bank
        self.target_accuracy = target_accuracy
        
        # Quiz state
        self.current_quiz: Dict = {}
        self.questions_presented: List[int] = []
        self.responses: List[Dict] = []
    
    def select_next_question(self, student_id: int, concept: str,
                            student_mastery: float,
                            previous_correct: bool = None) -> Question:
        """
        Select next question adaptively
        
        Args:
            student_id: Student identifier
            concept: Concept to quiz on
            student_mastery: Current mastery probability (0-1)
            previous_correct: Whether previous answer was correct
            
        Returns:
            Selected Question object
        """
        candidate_questions = self.qbank.get_questions_by_concept(concept)
        
        if not candidate_questions:
            return None
        
        # Filter out already used questions
        available = [q for q in candidate_questions
                    if q.question_id not in self.questions_presented]
        
        if not available:
            available = candidate_questions
        
        # Adjust difficulty based on previous answer
        if previous_correct is not None:
            if previous_correct:
                # Correct: try harder question
                available.sort(key=lambda q: q.get_difficulty_score(), reverse=True)
            else:
                # Incorrect: try easier question
                available.sort(key=lambda q: q.get_difficulty_score())
        else:
            # Initial question: match difficulty to mastery
            # Higher mastery = try harder questions
            available.sort(
                key=lambda q: abs(q.get_difficulty_score() - (student_mastery * 3))
            )
        
        selected = available[0]
        self.questions_presented.append(selected.question_id)
        return selected
    
    def record_response(self, question_id: int, student_id: int,
                       is_correct: int, time_spent: int) -> Dict:
        """
        Record quiz response and determine next action
        
        Args:
            question_id: Question ID
            student_id: Student ID
            is_correct: 1 if correct, 0 if incorrect
            time_spent: Time spent in seconds
            
        Returns:
            Response dict with feedback
        """
        question = self.qbank.get_question_by_id(question_id)
        
        if not question:
            return None
        
        # Update question statistics
        self.qbank.update_question_statistics(question_id, is_correct, time_spent)
        
        # Record response
        response = {
            'question_id': question_id,
            'student_id': student_id,
            'is_correct': is_correct,
            'time_spent': time_spent,
            'concept': question.concept,
            'difficulty': question.difficulty
        }
        
        self.responses.append(response)
        
        # Generate feedback
        feedback = self._generate_feedback(question, is_correct, time_spent)
        
        return {
            'response': response,
            'feedback': feedback,
            'next_action': 'continue' if len(self.responses) < 10 else 'complete'
        }
    
    def _generate_feedback(self, question: Question, is_correct: int,
                         time_spent: int) -> str:
        """Generate immediate feedback for question"""
        feedback = ""
        
        if is_correct:
            feedback = "✓ Correct! Well done!"
        else:
            feedback = "✗ Incorrect. Keep practicing!"
        
        # Time-based feedback
        if time_spent > question.estimated_time * 1.5:
            feedback += " (You spent extra time on this - consider reviewing the concept)"
        elif time_spent < question.estimated_time * 0.5:
            feedback += " (Fast attempt - make sure you understand the concept)"
        
        return feedback
    
    def get_quiz_statistics(self) -> Dict:
        """Get statistics for current quiz session"""
        if not self.responses:
            return {}
        
        responses_df = pd.DataFrame(self.responses)
        
        return {
            'total_questions': len(self.responses),
            'correct_answers': responses_df['is_correct'].sum(),
            'accuracy': responses_df['is_correct'].mean(),
            'avg_time_spent': responses_df['time_spent'].mean(),
            'concept_performance': responses_df.groupby('concept')['is_correct'].agg(['sum', 'count', 'mean']).to_dict(),
            'difficulty_distribution': responses_df['difficulty'].value_counts().to_dict()
        }
    
    def should_continue_quiz(self) -> bool:
        """Determine if quiz should continue"""
        if len(self.responses) < 3:
            return True
        
        recent_accuracy = np.mean([r['is_correct'] for r in self.responses[-5:]])
        
        # Continue if unstable accuracy (not converged)
        if 0.3 < recent_accuracy < 0.8:
            return True
        
        # Stop if too many questions
        if len(self.responses) >= 10:
            return False
        
        return True
    
    def start_new_quiz(self):
        """Start a new quiz session"""
        self.current_quiz = {}
        self.questions_presented = []
        self.responses = []


class DifficultyAdaptor:
    """Adapts quiz difficulty based on performance"""
    
    def __init__(self, initial_difficulty: str = 'Medium'):
        """
        Initialize difficulty adaptor
        
        Args:
            initial_difficulty: Starting difficulty level
        """
        self.difficulty_levels = ['Easy', 'Medium', 'Hard']
        self.current_difficulty = initial_difficulty
        self.difficulty_idx = self.difficulty_levels.index(initial_difficulty)
        self.response_history: List[int] = []
    
    def get_next_difficulty(self, recent_accuracy: float) -> str:
        """
        Determine next difficulty based on recent accuracy
        
        Args:
            recent_accuracy: Recent accuracy (0-1)
            
        Returns:
            Next difficulty level
        """
        self.response_history.append(1 if recent_accuracy > 0.65 else 0)
        
        # Look at last 3 responses
        if len(self.response_history) >= 3:
            recent = self.response_history[-3:]
            
            if sum(recent) >= 2:  # 2 or 3 correct
                # Increase difficulty
                self.difficulty_idx = min(2, self.difficulty_idx + 1)
            elif sum(recent) == 0:  # All incorrect
                # Decrease difficulty
                self.difficulty_idx = max(0, self.difficulty_idx - 1)
            # else: maintain current difficulty
        
        self.current_difficulty = self.difficulty_levels[self.difficulty_idx]
        return self.current_difficulty
    
    def reset(self, initial_difficulty: str = 'Medium'):
        """Reset difficulty adaptor"""
        self.difficulty_idx = self.difficulty_levels.index(initial_difficulty)
        self.current_difficulty = initial_difficulty
        self.response_history = []


class QuizPerformanceAnalyzer:
    """Analyzes quiz performance and provides insights"""
    
    @staticmethod
    def identify_misconceptions(quiz_engine: AdaptiveQuizEngine,
                              qbank: QuestionBank) -> Dict[str, List[str]]:
        """
        Identify common misconceptions based on error patterns
        
        Args:
            quiz_engine: QuizEngine with recorded responses
            qbank: QuestionBank
            
        Returns:
            Dictionary mapping concepts to common errors
        """
        misconceptions = {}
        responses_df = pd.DataFrame(quiz_engine.responses)
        
        for concept in responses_df['concept'].unique():
            concept_errors = responses_df[
                (responses_df['concept'] == concept) & (responses_df['is_correct'] == 0)
            ]
            
            if len(concept_errors) > 0:
                misconceptions[concept] = concept_errors['question_id'].tolist()
        
        return misconceptions
    
    @staticmethod
    def generate_performance_report(quiz_engine: AdaptiveQuizEngine) -> str:
        """
        Generate readable performance report
        
        Args:
            quiz_engine: QuizEngine with responses
            
        Returns:
            Formatted performance report
        """
        if not quiz_engine.responses:
            return "No quiz responses recorded."
        
        stats = quiz_engine.get_quiz_statistics()
        
        report = f"""
        ╔════════════════════════════════════╗
        ║       QUIZ PERFORMANCE REPORT       ║
        ╚════════════════════════════════════╝
        
        Questions Attempted: {stats['total_questions']}
        Correct Answers: {stats['correct_answers']}/{stats['total_questions']}
        Accuracy: {stats['accuracy']:.1%}
        Average Time: {stats['avg_time_spent']:.0f} seconds
        
        Performance by Concept:
        """
        
        for concept, data in stats['concept_performance'].items():
            if 'mean' in data:
                report += f"\n        {concept}: {data['mean']:.1%} ({int(data['sum'])}/{int(data['count'])})"
        
        return report


if __name__ == '__main__':
    # Example usage
    qbank_data = pd.DataFrame({
        'question_id': range(1, 11),
        'concept': ['Concept_1'] * 5 + ['Concept_2'] * 5,
        'difficulty': ['Easy', 'Easy', 'Medium', 'Hard', 'Hard'] * 2,
        'bloom_level': ['Understand'] * 10,
        'avg_solve_time': [30] * 10
    })
    
    qbank = QuestionBank(qbank_data)
    quiz = AdaptiveQuizEngine(qbank)
    
    print("Adaptive Quiz Engine Initialized")
    print(f"Total questions in bank: {len(qbank.questions)}")
    
    # Start quiz
    quiz.start_new_quiz()
    
    # Select questions
    q1 = quiz.select_next_question(1, 'Concept_1', 0.5)
    print(f"\nSelected Question: ID {q1.question_id} ({q1.difficulty})")
    
    # Record response
    result = quiz.record_response(q1.question_id, 1, 1, 25)
    print(f"Response: {result['response']['is_correct']} Correct")
    print(f"Feedback: {result['feedback']}")
