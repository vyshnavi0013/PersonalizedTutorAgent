"""
Synthetic Quiz Interaction Dataset Generator
Generates student interaction logs for tutor agent training and evaluation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class SyntheticDatasetGenerator:
    """Generate realistic synthetic student quiz interaction data"""
    
    def __init__(self, n_students=50, n_concepts=10, n_questions=100, seed=42):
        """
        Initialize dataset generator
        
        Args:
            n_students: Number of students
            n_concepts: Number of learning concepts
            n_questions: Total questions in question bank
            seed: Random seed for reproducibility
        """
        np.random.seed(seed)
        random.seed(seed)
        
        self.n_students = n_students
        self.n_concepts = n_concepts
        self.n_questions = n_questions
        self.concepts = [f"Concept_{i+1}" for i in range(n_concepts)]
        self.difficulty_levels = ['Easy', 'Medium', 'Hard']
        
    def generate_question_bank(self):
        """Generate question bank with metadata"""
        questions = []
        for q_id in range(self.n_questions):
            questions.append({
                'question_id': q_id + 1,
                'concept': random.choice(self.concepts),
                'difficulty': random.choice(self.difficulty_levels),
                'bloom_level': random.choice(['Understand', 'Apply', 'Analyze', 'Evaluate']),
                'avg_solve_time': np.random.uniform(30, 300)  # seconds
            })
        return pd.DataFrame(questions)
    
    def _generate_student_profile(self, student_id):
        """Generate a unique learning profile for each student"""
        profile = {}
        for concept in self.concepts:
            profile[concept] = {
                'base_ability': np.random.uniform(0.3, 0.9),  # Ability to grasp concept
                'learning_rate': np.random.uniform(0.02, 0.15),  # How quickly they improve
                'fatigue_factor': np.random.uniform(0.95, 1.0),  # Fatigue effect on performance
                'concept_affinity': np.random.uniform(0.0, 1.0)  # Natural preference
            }
        return profile
    
    def _calculate_question_difficulty_score(self, difficulty):
        """Map difficulty to numeric score"""
        difficulty_map = {'Easy': 1, 'Medium': 2, 'Hard': 3}
        return difficulty_map[difficulty]
    
    def _predict_student_performance(self, student_profile, concept, attempt_no, difficulty):
        """
        Predict student performance on question
        Incorporates: ability, learning over attempts, fatigue, difficulty
        """
        profile = student_profile[concept]
        base_ability = profile['base_ability']
        
        # Improvement with attempts (learning)
        attempt_bonus = min(0.2, (attempt_no - 1) * profile['learning_rate'])
        
        # Fatigue factor (decreases with more questions)
        fatigue = profile['fatigue_factor'] ** (attempt_no - 1)
        
        # Difficulty impact
        difficulty_score = self._calculate_question_difficulty_score(difficulty)
        difficulty_penalty = 0.25 * (difficulty_score - 1)  # Hard is 0.5 penalty
        
        # Final probability of correctness
        prob_correct = base_ability + attempt_bonus - difficulty_penalty
        prob_correct = np.clip(prob_correct * fatigue, 0.1, 0.95)
        
        return prob_correct
    
    def generate_interactions(self, qbank, n_interactions_per_student=50):
        """
        Generate student quiz interactions
        
        Args:
            qbank: Question bank DataFrame
            n_interactions_per_student: Number of interactions per student
            
        Returns:
            DataFrame with interaction records
        """
        interactions = []
        
        for student_id in range(1, self.n_students + 1):
            # Generate unique profile for this student
            student_profile = self._generate_student_profile(student_id)
            
            # Generate interactions for this student
            for interaction_idx in range(n_interactions_per_student):
                # Select a random question
                q_row = qbank.sample(1).iloc[0]
                question_id = q_row['question_id']
                concept = q_row['concept']
                difficulty = q_row['difficulty']
                
                # Determine attempt number (usually 1-2, occasionally more)
                attempt_no = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
                
                # Predict performance
                prob_correct = self._predict_student_performance(
                    student_profile, concept, attempt_no, difficulty
                )
                
                # Sample actual score
                score = 1 if np.random.rand() < prob_correct else 0
                
                # Time spent (with variance)
                base_time = q_row['avg_solve_time']
                time_factor = 1.2 if score == 0 else 0.8  # Wrong answers take longer
                time_spent = base_time * time_factor * np.random.uniform(0.7, 1.3)
                
                # Timestamp (simulate temporal sequence)
                timestamp = datetime.now() - timedelta(
                    days=n_interactions_per_student - interaction_idx,
                    hours=np.random.randint(0, 24)
                )
                
                interactions.append({
                    'student_id': student_id,
                    'question_id': question_id,
                    'concept': concept,
                    'difficulty': difficulty,
                    'score': score,  # 1 = correct, 0 = incorrect
                    'time_spent': int(time_spent),
                    'attempt_no': attempt_no,
                    'timestamp': timestamp
                })
        
        df = pd.DataFrame(interactions)
        df = df.sort_values('timestamp').reset_index(drop=True)
        return df
    
    def generate_complete_dataset(self, n_interactions_per_student=50):
        """Generate complete dataset with question bank and interactions"""
        print("Generating question bank...")
        qbank = self.generate_question_bank()
        
        print(f"Generating {self.n_students} students × {n_interactions_per_student} interactions...")
        interactions = self.generate_interactions(qbank, n_interactions_per_student)
        
        return qbank, interactions


def save_datasets(qbank, interactions, data_dir='data'):
    """Save question bank and interactions to CSV"""
    qbank.to_csv(f'{data_dir}/question_bank.csv', index=False)
    interactions.to_csv(f'{data_dir}/student_interactions.csv', index=False)
    print(f"✓ Question bank saved: {data_dir}/question_bank.csv")
    print(f"✓ Student interactions saved: {data_dir}/student_interactions.csv")
    print(f"  - {len(interactions)} total interactions")
    print(f"  - {interactions['student_id'].nunique()} unique students")
    print(f"  - {interactions['concept'].nunique()} unique concepts")


def get_dataset_statistics(qbank, interactions):
    """Print dataset statistics"""
    print("\n" + "="*60)
    print("DATASET STATISTICS")
    print("="*60)
    
    print(f"\nQuestion Bank:")
    print(f"  - Total questions: {len(qbank)}")
    print(f"  - Concepts: {qbank['concept'].nunique()}")
    print(f"  - Difficulty distribution:\n{qbank['difficulty'].value_counts()}")
    
    print(f"\nStudent Interactions:")
    print(f"  - Total interactions: {len(interactions)}")
    print(f"  - Unique students: {interactions['student_id'].nunique()}")
    print(f"  - Average interactions per student: {len(interactions) / interactions['student_id'].nunique():.1f}")
    print(f"  - Overall correctness rate: {interactions['score'].mean():.2%}")
    print(f"  - Average time spent: {interactions['time_spent'].mean():.0f} seconds")
    
    print(f"\nConcept-wise Performance:")
    concept_perf = interactions.groupby('concept').agg({
        'score': ['count', 'mean'],
        'time_spent': 'mean'
    }).round(3)
    print(concept_perf)
    
    print("\n" + "="*60)


if __name__ == '__main__':
    # Generate datasets
    generator = SyntheticDatasetGenerator(n_students=50, n_concepts=8, n_questions=80)
    qbank, interactions = generator.generate_complete_dataset(n_interactions_per_student=60)
    
    # Save to files
    save_datasets(qbank, interactions, data_dir='.')
    
    # Print statistics
    get_dataset_statistics(qbank, interactions)
