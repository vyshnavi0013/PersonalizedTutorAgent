"""
Knowledge Tracing Module
Simplified Deep Knowledge Tracing (DKT) for predicting student mastery
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')


class SimplifiedDKT:
    """
    Simplified Deep Knowledge Tracing
    Uses probabilistic Bayesian approach instead of LSTM for mini-project level
    Suitable for IIT/NIT academic project standards
    """
    
    def __init__(self, concepts: List[str], learning_rate: float = 0.1, 
                 forget_rate: float = 0.05):
        """
        Initialize Simplified DKT
        
        Args:
            concepts: List of concept names
            learning_rate: Learning coefficient (0-1)
            forget_rate: Forgetting coefficient (0-1)
        """
        self.concepts = concepts
        self.learning_rate = learning_rate
        self.forget_rate = forget_rate
        
        # Initial knowledge state (uninformed prior)
        self.initial_knowledge = {concept: 0.3 for concept in concepts}
        
        # Transition probabilities
        self.transition_matrix = self._initialize_transitions()
        
    def _initialize_transitions(self) -> Dict[str, Dict[str, float]]:
        """
        Initialize state transition matrices
        For each concept, define probability of:
        - Knowledge improvement when correct
        - Knowledge retention when incorrect
        """
        transitions = {}
        for concept in self.concepts:
            transitions[concept] = {
                'p_learn': self.learning_rate,      # P(learn | correct)
                'p_forget': self.forget_rate,       # P(forget | incorrect)
                'p_correct_know': 0.9,              # P(correct | knows)
                'p_correct_unknown': 0.1            # P(correct | guessing)
            }
        return transitions
    
    def predict_next_state(self, current_knowledge: Dict[str, float],
                          concept: str, is_correct: int) -> Dict[str, float]:
        """
        Predict next knowledge state after attempt
        
        Args:
            current_knowledge: Current mastery probabilities
            concept: Concept being learned
            is_correct: 1 if correct, 0 if incorrect
            
        Returns:
            Updated knowledge state
        """
        next_knowledge = current_knowledge.copy()
        trans = self.transition_matrix[concept]
        
        current_mastery = current_knowledge[concept]
        
        if is_correct:
            # Correct answer: increase mastery
            improvement = (1 - current_mastery) * trans['p_learn']
            next_knowledge[concept] = min(1.0, current_mastery + improvement)
        else:
            # Incorrect answer: decrease mastery slightly
            decay = current_mastery * trans['p_forget']
            next_knowledge[concept] = max(0.0, current_mastery - decay)
        
        return next_knowledge
    
    def trace_student(self, student_interactions: pd.DataFrame,
                     student_id: int) -> Tuple[List[Dict], Dict[str, float]]:
        """
        Trace knowledge state trajectory for a student
        
        Args:
            student_interactions: DataFrame with student's interactions
            student_id: Student ID
            
        Returns:
            Tuple of (trajectory list, final knowledge state)
        """
        # Filter interactions for this student, sorted by timestamp
        student_data = student_interactions[
            student_interactions['student_id'] == student_id
        ].sort_values('timestamp').reset_index(drop=True)
        
        # Initialize knowledge state
        knowledge = self.initial_knowledge.copy()
        trajectory = []
        
        for _, row in student_data.iterrows():
            concept = row['concept']
            correct = row['score']
            
            # Record state before interaction
            trajectory.append({
                'timestamp': row['timestamp'],
                'concept': concept,
                'is_correct': correct,
                'knowledge_before': knowledge[concept],
                'all_knowledge_before': knowledge.copy()
            })
            
            # Update knowledge state
            knowledge = self.predict_next_state(knowledge, concept, correct)
            trajectory[-1]['knowledge_after'] = knowledge[concept]
        
        return trajectory, knowledge
    
    def predict_performance(self, knowledge_state: Dict[str, float],
                           concept: str) -> float:
        """
        Predict probability of student answering correctly
        Based on current knowledge state
        
        Args:
            knowledge_state: Current knowledge state
            concept: Target concept
            
        Returns:
            Probability of correct answer
        """
        trans = self.transition_matrix[concept]
        mastery = knowledge_state[concept]
        
        # P(correct) = P(correct|know) * P(know) + P(correct|don't know) * P(don't know)
        prob_correct = (
            trans['p_correct_know'] * mastery + 
            trans['p_correct_unknown'] * (1 - mastery)
        )
        
        return prob_correct
    
    def estimate_steps_to_mastery(self, current_knowledge: Dict[str, float],
                                  concept: str, 
                                  mastery_threshold: float = 0.8) -> int:
        """
        Estimate number of correct attempts needed to reach mastery
        
        Args:
            current_knowledge: Current mastery state
            concept: Target concept
            mastery_threshold: Target mastery level
            
        Returns:
            Estimated number of correct attempts
        """
        mastery = current_knowledge[concept]
        
        if mastery >= mastery_threshold:
            return 0
        
        trans = self.transition_matrix[concept]
        steps = 0
        temp_mastery = mastery
        
        while temp_mastery < mastery_threshold and steps < 100:
            improvement = (1 - temp_mastery) * trans['p_learn']
            temp_mastery += improvement
            steps += 1
        
        return steps
    
    def calculate_concept_difficulty(self, student_interactions: pd.DataFrame,
                                    concept: str) -> float:
        """
        Calculate perceived difficulty of concept for students
        Based on error rates and improvement speed
        
        Args:
            student_interactions: Interaction dataframe
            concept: Target concept
            
        Returns:
            Difficulty score (0-1, where 1 is hardest)
        """
        concept_data = student_interactions[
            student_interactions['concept'] == concept
        ]
        
        if len(concept_data) == 0:
            return 0.5
        
        error_rate = 1 - concept_data['score'].mean()
        
        # Average attempt number to first success per student
        attempts_to_success = concept_data.groupby('student_id').apply(
            lambda x: (x['score'] == 0).sum() if (x['score'] == 1).any() else x.shape[0]
        )
        
        avg_attempts = attempts_to_success.mean()
        attempt_ratio = min(1.0, avg_attempts / 5.0)  # Normalize
        
        # Difficulty = error rate + attempts needed
        difficulty = (error_rate * 0.6 + attempt_ratio * 0.4)
        
        return np.clip(difficulty, 0.0, 1.0)
    
    def get_concept_readiness(self, current_knowledge: Dict[str, float],
                            student_interactions: pd.DataFrame,
                            prerequisite_map: Dict[str, List[str]] = None) -> Dict[str, float]:
        """
        Determine readiness for each concept based on prerequisites
        
        Args:
            current_knowledge: Current knowledge state
            student_interactions: Historical interactions
            prerequisite_map: Mapping of concepts to prerequisites
            
        Returns:
            Readiness score for each concept
        """
        if prerequisite_map is None:
            prerequisite_map = {}
        
        readiness = {}
        
        for concept in self.concepts:
            base_readiness = current_knowledge.get(concept, 0.3)
            
            # Check prerequisites
            prerequisites = prerequisite_map.get(concept, [])
            if prerequisites:
                prereq_mastery = np.mean([
                    current_knowledge.get(p, 0.3) for p in prerequisites
                ])
                # Need 60% mastery of prerequisites
                if prereq_mastery < 0.6:
                    base_readiness *= 0.5
            
            readiness[concept] = base_readiness
        
        return readiness


class KnowledgeTracingEvaluator:
    """Evaluate DKT performance"""
    
    @staticmethod
    def calculate_prediction_accuracy(dkt: SimplifiedDKT,
                                    student_interactions: pd.DataFrame,
                                    student_id: int,
                                    lookahead: int = 1) -> float:
        """
        Calculate DKT prediction accuracy for a student
        
        Args:
            dkt: Initialized SimplifiedDKT model
            student_interactions: Interaction dataframe
            student_id: Target student
            lookahead: Number of steps ahead to predict
            
        Returns:
            Accuracy of predictions
        """
        student_data = student_interactions[
            student_interactions['student_id'] == student_id
        ].sort_values('timestamp').reset_index(drop=True)
        
        if len(student_data) < lookahead + 1:
            return 0.0
        
        knowledge = dkt.initial_knowledge.copy()
        correct_predictions = 0
        total_predictions = 0
        
        for i in range(len(student_data) - lookahead):
            # Make prediction for future concept
            future_concept = student_data.iloc[i + lookahead]['concept']
            actual_correct = student_data.iloc[i + lookahead]['score']
            
            # Predict performance
            pred_prob = dkt.predict_performance(knowledge, future_concept)
            pred_correct = 1 if pred_prob > 0.5 else 0
            
            if pred_correct == actual_correct:
                correct_predictions += 1
            total_predictions += 1
            
            # Update knowledge after each interaction
            concept = student_data.iloc[i]['concept']
            correct = student_data.iloc[i]['score']
            knowledge = dkt.predict_next_state(knowledge, concept, correct)
        
        return correct_predictions / total_predictions if total_predictions > 0 else 0.0


if __name__ == '__main__':
    # Example usage
    concepts = ['Concept_1', 'Concept_2', 'Concept_3']
    dkt = SimplifiedDKT(concepts)
    
    # Test with sample data
    test_data = pd.DataFrame({
        'student_id': [1, 1, 1, 1, 1],
        'concept': ['Concept_1', 'Concept_1', 'Concept_2', 'Concept_1', 'Concept_2'],
        'score': [1, 1, 0, 1, 1],
        'timestamp': pd.date_range('2024-01-01', periods=5),
        'time_spent': [45, 50, 60, 40, 55]
    })
    
    # Trace student
    trajectory, final_knowledge = dkt.trace_student(test_data, student_id=1)
    
    print("Knowledge Trajectory:")
    for step in trajectory:
        print(f"  {step['concept']}: {step['knowledge_before']:.3f} -> {step['knowledge_after']:.3f} " +
              f"(Correct: {step['is_correct']})")
    
    print(f"\nFinal Knowledge State: {final_knowledge}")
    
    # Estimate mastery time
    for concept in concepts:
        steps = dkt.estimate_steps_to_mastery(final_knowledge, concept)
        print(f"  {concept}: ~{steps} more correct attempts to mastery")
