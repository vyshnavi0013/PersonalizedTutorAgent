"""
Learner Profiling Module
Tracks student performance and maintains learner knowledge state vector
"""

import pandas as pd
import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple


class LearnerProfile:
    """Maintains learner profiling information"""
    
    def __init__(self, student_id: int, concepts: List[str]):
        """
        Initialize learner profile
        
        Args:
            student_id: Unique student identifier
            concepts: List of concept names
        """
        self.student_id = student_id
        self.concepts = concepts
        
        # Performance metrics per concept
        self.concept_metrics = defaultdict(lambda: {
            'attempts': 0,
            'correct': 0,
            'incorrect': 0,
            'total_time': 0,
            'avg_difficulty_faced': 0.0,
            'last_attempt_timestamp': None,
            'streak': 0  # Consecutive correct answers
        })
        
        # Overall learner metrics
        self.overall_metrics = {
            'total_questions': 0,
            'total_correct': 0,
            'total_attempts': 0,
            'total_time_spent': 0,
            'average_accuracy': 0.0,
            'learning_velocity': 0.0
        }
        
        # Knowledge state vector (mastery probability per concept)
        self.knowledge_state = {concept: 0.0 for concept in concepts}
        
    def update_with_interaction(self, concept: str, correct: int, 
                               time_spent: int, difficulty: str, timestamp=None):
        """
        Update profile with new interaction
        
        Args:
            concept: Concept name
            correct: 1 if correct, 0 if incorrect
            time_spent: Time spent in seconds
            difficulty: Difficulty level (Easy/Medium/Hard)
            timestamp: Timestamp of interaction
        """
        metrics = self.concept_metrics[concept]
        
        # Update attempt counts
        metrics['attempts'] += 1
        metrics['correct'] += correct
        metrics['incorrect'] += 1 - correct
        metrics['total_time'] += time_spent
        metrics['last_attempt_timestamp'] = timestamp
        
        # Update streak
        if correct:
            metrics['streak'] += 1
        else:
            metrics['streak'] = 0
        
        # Track difficulty progression
        difficulty_map = {'Easy': 1, 'Medium': 2, 'Hard': 3}
        diff_score = difficulty_map.get(difficulty, 2)
        metrics['avg_difficulty_faced'] = (
            (metrics['avg_difficulty_faced'] * (metrics['attempts'] - 1) + diff_score) / 
            metrics['attempts']
        )
        
        # Update overall metrics
        self.overall_metrics['total_questions'] += 1
        self.overall_metrics['total_correct'] += correct
        self.overall_metrics['total_attempts'] += 1
        self.overall_metrics['total_time_spent'] += time_spent
        self.overall_metrics['average_accuracy'] = (
            self.overall_metrics['total_correct'] / self.overall_metrics['total_questions']
        )
    
    def calculate_mastery_probability(self, concept: str, 
                                     threshold: float = 0.7) -> float:
        """
        Calculate mastery probability for a concept
        Based on accuracy, recency, and effort
        
        Args:
            concept: Concept name
            threshold: Performance threshold for mastery
            
        Returns:
            Mastery probability (0-1)
        """
        if concept not in self.concept_metrics or self.concept_metrics[concept]['attempts'] == 0:
            return 0.0
        
        metrics = self.concept_metrics[concept]
        
        # Accuracy component (0-1)
        if metrics['attempts'] > 0:
            accuracy = metrics['correct'] / metrics['attempts']
        else:
            accuracy = 0.0
        
        # Recency bonus (encourages recent practice)
        # Streak component (consecutive correct answers)
        streak_bonus = min(0.1, metrics['streak'] * 0.05)
        
        # Effort component (more attempts on difficult topics shows engagement)
        effort_weight = min(1.0, metrics['attempts'] / 10.0) * 0.1
        
        # Combine components
        mastery = accuracy + streak_bonus + effort_weight
        mastery = np.clip(mastery, 0.0, 1.0)
        
        return mastery
    
    def get_knowledge_state_vector(self) -> Dict[str, float]:
        """
        Get current knowledge state vector
        Maps each concept to mastery probability
        
        Returns:
            Dictionary mapping concepts to mastery probabilities
        """
        for concept in self.concepts:
            self.knowledge_state[concept] = self.calculate_mastery_probability(concept)
        return self.knowledge_state
    
    def get_weak_concepts(self, n: int = 3, threshold: float = 0.6) -> List[str]:
        """
        Get weakest concepts for a learner
        
        Args:
            n: Number of weak concepts to return
            threshold: Mastery threshold below which concepts are weak
            
        Returns:
            List of weak concepts sorted by mastery (lowest first)
        """
        knowledge = self.get_knowledge_state_vector()
        weak = [(c, m) for c, m in knowledge.items() if m < threshold]
        weak.sort(key=lambda x: x[1])
        return [c for c, _ in weak[:n]]
    
    def get_strong_concepts(self, n: int = 3, threshold: float = 0.75) -> List[str]:
        """
        Get strongest concepts for a learner
        
        Args:
            n: Number of strong concepts to return
            threshold: Mastery threshold above which concepts are strong
            
        Returns:
            List of strong concepts sorted by mastery (highest first)
        """
        knowledge = self.get_knowledge_state_vector()
        strong = [(c, m) for c, m in knowledge.items() if m >= threshold]
        strong.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in strong[:n]]
    
    def get_concept_statistics(self, concept: str) -> Dict:
        """Get detailed statistics for a specific concept"""
        if concept not in self.concept_metrics:
            return None
        
        metrics = self.concept_metrics[concept]
        return {
            'concept': concept,
            'total_attempts': metrics['attempts'],
            'correct_attempts': metrics['correct'],
            'accuracy': metrics['correct'] / metrics['attempts'] if metrics['attempts'] > 0 else 0.0,
            'avg_time_spent': metrics['total_time'] / metrics['attempts'] if metrics['attempts'] > 0 else 0,
            'difficulty_faced': metrics['avg_difficulty_faced'],
            'current_streak': metrics['streak'],
            'mastery_probability': self.calculate_mastery_probability(concept)
        }
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary for serialization"""
        return {
            'student_id': self.student_id,
            'overall_metrics': self.overall_metrics,
            'concept_metrics': dict(self.concept_metrics),
            'knowledge_state': self.get_knowledge_state_vector()
        }


class LearnerProfileManager:
    """Manages profiles for multiple learners"""
    
    def __init__(self, concepts: List[str]):
        """
        Initialize profile manager
        
        Args:
            concepts: List of concept names
        """
        self.concepts = concepts
        self.profiles: Dict[int, LearnerProfile] = {}
    
    def get_or_create_profile(self, student_id: int) -> LearnerProfile:
        """Get existing profile or create new one"""
        if student_id not in self.profiles:
            self.profiles[student_id] = LearnerProfile(student_id, self.concepts)
        return self.profiles[student_id]
    
    def update_from_interactions(self, interactions_df: pd.DataFrame):
        """
        Update all profiles from interaction dataframe
        
        Args:
            interactions_df: DataFrame with columns:
                student_id, concept, score, time_spent, difficulty, timestamp
        """
        for _, row in interactions_df.iterrows():
            profile = self.get_or_create_profile(row['student_id'])
            profile.update_with_interaction(
                concept=row['concept'],
                correct=row['score'],
                time_spent=row['time_spent'],
                difficulty=row['difficulty'],
                timestamp=row.get('timestamp')
            )
    
    def get_learner_profiles_summary(self) -> pd.DataFrame:
        """
        Get summary of all learner profiles
        
        Returns:
            DataFrame with learner statistics
        """
        summaries = []
        for student_id, profile in self.profiles.items():
            knowledge = profile.get_knowledge_state_vector()
            avg_mastery = np.mean(list(knowledge.values()))
            
            summaries.append({
                'student_id': student_id,
                'total_questions': profile.overall_metrics['total_questions'],
                'overall_accuracy': profile.overall_metrics['average_accuracy'],
                'average_mastery': avg_mastery,
                'total_time_spent': profile.overall_metrics['total_time_spent'],
                'weak_concepts': ', '.join(profile.get_weak_concepts(n=2)),
                'strong_concepts': ', '.join(profile.get_strong_concepts(n=2))
            })
        
        return pd.DataFrame(summaries)
    
    def export_profiles(self) -> Dict:
        """Export all profiles"""
        return {sid: prof.to_dict() for sid, prof in self.profiles.items()}


if __name__ == '__main__':
    # Example usage
    concepts = ['Concept_1', 'Concept_2', 'Concept_3']
    
    # Create manager and some test data
    manager = LearnerProfileManager(concepts)
    
    # Simulate interactions
    test_interactions = pd.DataFrame({
        'student_id': [1, 1, 1, 2, 2, 2],
        'concept': ['Concept_1', 'Concept_1', 'Concept_2', 'Concept_1', 'Concept_2', 'Concept_3'],
        'score': [1, 1, 0, 1, 1, 0],
        'time_spent': [45, 50, 60, 40, 55, 70],
        'difficulty': ['Easy', 'Medium', 'Hard', 'Easy', 'Medium', 'Hard']
    })
    
    manager.update_from_interactions(test_interactions)
    
    # Display results
    print("Learner Profiles Summary:")
    print(manager.get_learner_profiles_summary())
    
    print("\nDetailed Profile - Student 1:")
    profile_1 = manager.profiles[1]
    print(f"Knowledge State: {profile_1.get_knowledge_state_vector()}")
    print(f"Weak Concepts: {profile_1.get_weak_concepts()}")
    print(f"Strong Concepts: {profile_1.get_strong_concepts()}")
