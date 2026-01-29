"""
Learning Path Generator
Generates personalized learning paths based on student knowledge and mastery
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
import heapq


@dataclass
class LearningNode:
    """Represents a concept in the learning path"""
    concept: str
    difficulty: float
    prerequisites: List[str]
    estimated_time: int  # minutes
    mastery_level: float = 0.0
    priority: float = 0.0


class LearningPathGenerator:
    """
    Generates personalized learning paths based on:
    - Current knowledge state
    - Concept difficulty
    - Prerequisites
    - Learner preferences
    """
    
    def __init__(self, concepts: List[str], 
                 concept_difficulty: Dict[str, float] = None,
                 prerequisites: Dict[str, List[str]] = None,
                 estimated_times: Dict[str, int] = None):
        """
        Initialize learning path generator
        
        Args:
            concepts: List of all available concepts
            concept_difficulty: Difficulty score for each concept (0-1)
            prerequisites: Prerequisites for each concept
            estimated_times: Estimated learning time in minutes
        """
        self.concepts = concepts
        
        # Default difficulty is moderate
        self.concept_difficulty = concept_difficulty or {
            c: 0.5 for c in concepts
        }
        
        # Default no prerequisites
        self.prerequisites = prerequisites or {
            c: [] for c in concepts
        }
        
        # Default estimated time
        self.estimated_times = estimated_times or {
            c: 30 for c in concepts
        }
    
    def generate_path(self, student_knowledge: Dict[str, float],
                     weak_concepts: List[str] = None,
                     num_concepts: int = 5,
                     max_difficulty: float = 0.8,
                     learning_preference: str = 'balanced') -> List[Dict]:
        """
        Generate personalized learning path
        
        Args:
            student_knowledge: Current mastery for each concept
            weak_concepts: Concepts student struggles with
            num_concepts: Number of concepts to include in path
            max_difficulty: Maximum difficulty to include
            learning_preference: 'balanced', 'progressive', or 'review'
            
        Returns:
            List of learning path nodes
        """
        path = []
        candidate_concepts = []
        
        # Score each concept for inclusion in path
        for concept in self.concepts:
            # Skip if already mastered
            if student_knowledge.get(concept, 0.0) >= 0.85:
                continue
            
            # Skip if too difficult
            if self.concept_difficulty[concept] > max_difficulty:
                continue
            
            # Check prerequisites
            prereqs_met = self._check_prerequisites_met(
                concept, student_knowledge
            )
            if not prereqs_met:
                continue
            
            # Calculate priority score
            priority = self._calculate_concept_priority(
                concept, student_knowledge, weak_concepts, learning_preference
            )
            
            candidate_concepts.append((concept, priority))
        
        # Sort by priority (higher first)
        candidate_concepts.sort(key=lambda x: x[1], reverse=True)
        
        # Select top concepts
        selected = [c for c, _ in candidate_concepts[:num_concepts]]
        
        # Order selected concepts
        path = self._topological_sort_concepts(selected, student_knowledge)
        
        return path
    
    def _check_prerequisites_met(self, concept: str,
                                student_knowledge: Dict[str, float],
                                mastery_threshold: float = 0.6) -> bool:
        """
        Check if prerequisites are met for a concept
        
        Args:
            concept: Target concept
            student_knowledge: Current knowledge state
            mastery_threshold: Required mastery of prerequisites
            
        Returns:
            True if prerequisites are met
        """
        prerequisites = self.prerequisites.get(concept, [])
        
        if not prerequisites:
            return True
        
        for prereq in prerequisites:
            if student_knowledge.get(prereq, 0.0) < mastery_threshold:
                return False
        
        return True
    
    def _calculate_concept_priority(self, concept: str,
                                   student_knowledge: Dict[str, float],
                                   weak_concepts: List[str] = None,
                                   preference: str = 'balanced') -> float:
        """
        Calculate priority score for concept inclusion
        
        Args:
            concept: Target concept
            student_knowledge: Current knowledge state
            weak_concepts: List of weak concepts
            preference: Learning preference
            
        Returns:
            Priority score (higher = higher priority)
        """
        current_mastery = student_knowledge.get(concept, 0.0)
        difficulty = self.concept_difficulty[concept]
        
        # Base priority: inverse of mastery (need to learn weak concepts)
        mastery_gap = 1.0 - current_mastery
        
        if preference == 'balanced':
            # Mix of difficulty and mastery gap
            priority = (0.5 * mastery_gap) + (0.3 * difficulty)
            
            # Boost weak concepts
            if weak_concepts and concept in weak_concepts:
                priority *= 1.3
        
        elif preference == 'progressive':
            # Increase difficulty gradually
            priority = (0.4 * mastery_gap) + (0.6 * difficulty)
        
        elif preference == 'review':
            # Focus on weak concepts first
            priority = mastery_gap
            if weak_concepts and concept in weak_concepts:
                priority *= 2.0
        
        else:
            priority = mastery_gap
        
        return priority
    
    def _topological_sort_concepts(self, concepts: List[str],
                                  student_knowledge: Dict[str, float]) -> List[Dict]:
        """
        Sort concepts respecting prerequisites
        Easier concepts first, then progress to harder
        
        Args:
            concepts: Concepts to sort
            student_knowledge: Current knowledge state
            
        Returns:
            Sorted list of concept nodes
        """
        # Build dependency graph for selected concepts
        concept_set = set(concepts)
        
        # Add prerequisites that are in the concept set
        for concept in concepts:
            for prereq in self.prerequisites.get(concept, []):
                if prereq in concept_set:
                    # Prerequisites already satisfied, no need to add
                    pass
        
        # Sort by: prerequisites first, then difficulty, then mastery gap
        def sort_key(concept):
            prereq_count = len([p for p in self.prerequisites.get(concept, [])
                              if p in concept_set])
            difficulty = self.concept_difficulty[concept]
            mastery_gap = 1.0 - student_knowledge.get(concept, 0.0)
            
            # Tuples are compared lexicographically
            return (prereq_count, difficulty, -mastery_gap)
        
        sorted_concepts = sorted(concepts, key=sort_key)
        
        # Create learning path nodes
        path = []
        for idx, concept in enumerate(sorted_concepts):
            node = {
                'position': idx + 1,
                'concept': concept,
                'difficulty': self.concept_difficulty[concept],
                'current_mastery': student_knowledge.get(concept, 0.0),
                'estimated_time': self.estimated_times.get(concept, 30),
                'prerequisites': self.prerequisites.get(concept, []),
                'bloom_level': self._estimate_bloom_level(concept, student_knowledge),
                'resources': self._suggest_resources(concept)
            }
            path.append(node)
        
        return path
    
    def _estimate_bloom_level(self, concept: str,
                            student_knowledge: Dict[str, float]) -> str:
        """
        Estimate appropriate Bloom's taxonomy level
        Based on current mastery
        
        Args:
            concept: Target concept
            student_knowledge: Current knowledge state
            
        Returns:
            Bloom level (Remember, Understand, Apply, Analyze, Evaluate, Create)
        """
        mastery = student_knowledge.get(concept, 0.0)
        
        if mastery < 0.2:
            return "Remember"
        elif mastery < 0.4:
            return "Understand"
        elif mastery < 0.6:
            return "Apply"
        elif mastery < 0.75:
            return "Analyze"
        elif mastery < 0.9:
            return "Evaluate"
        else:
            return "Create"
    
    def _suggest_resources(self, concept: str) -> List[str]:
        """
        Suggest learning resources for a concept
        
        Args:
            concept: Target concept
            
        Returns:
            List of suggested resource types
        """
        resources = ["Video Lecture", "Reading Material", "Practice Problems"]
        
        # Customize based on difficulty
        difficulty = self.concept_difficulty[concept]
        if difficulty > 0.7:
            resources.append("Expert Explanation")
            resources.append("Step-by-step Tutorial")
        
        return resources
    
    def adapt_path(self, current_path: List[Dict],
                  latest_performance: Dict[str, float],
                  adaptive_mode: str = 'dynamic') -> List[Dict]:
        """
        Adapt learning path based on performance
        
        Args:
            current_path: Current learning path
            latest_performance: Recent performance metrics
            adaptive_mode: 'dynamic' (frequent updates) or 'scheduled'
            
        Returns:
            Adapted learning path
        """
        adapted_path = []
        
        for node in current_path:
            concept = node['concept']
            new_mastery = latest_performance.get(concept, node['current_mastery'])
            
            # Update mastery
            node['current_mastery'] = new_mastery
            
            # Update Bloom level
            node['bloom_level'] = self._estimate_bloom_level(concept, 
                                                            {concept: new_mastery})
            
            # Decide if should remove concept or adjust difficulty
            if new_mastery >= 0.85:
                # Concept mastered, mark for completion
                node['status'] = 'completed'
            else:
                node['status'] = 'in-progress'
            
            adapted_path.append(node)
        
        return adapted_path
    
    def get_next_concept(self, current_path: List[Dict],
                        current_mastery: Dict[str, float]) -> Dict:
        """
        Get the next concept to study in the path
        
        Args:
            current_path: Current learning path
            current_mastery: Latest mastery levels
            
        Returns:
            Next concept node or None if path complete
        """
        for node in current_path:
            concept = node['concept']
            mastery = current_mastery.get(concept, 0.0)
            
            if mastery < 0.85:
                return node
        
        return None
    
    def estimate_path_duration(self, path: List[Dict]) -> int:
        """
        Estimate total time to complete learning path
        
        Args:
            path: Learning path
            
        Returns:
            Estimated time in minutes
        """
        total_time = sum(node['estimated_time'] for node in path)
        return total_time


class AdaptivePathManager:
    """Manages learning paths for multiple students"""
    
    def __init__(self, path_generator: LearningPathGenerator):
        """
        Initialize adaptive path manager
        
        Args:
            path_generator: LearningPathGenerator instance
        """
        self.path_generator = path_generator
        self.student_paths: Dict[int, List[Dict]] = {}
        self.path_history: Dict[int, List[List[Dict]]] = {}
    
    def create_initial_path(self, student_id: int,
                           student_knowledge: Dict[str, float],
                           weak_concepts: List[str] = None) -> List[Dict]:
        """Create initial learning path for student"""
        path = self.path_generator.generate_path(
            student_knowledge, weak_concepts, num_concepts=5
        )
        
        self.student_paths[student_id] = path
        self.path_history[student_id] = [path.copy()]
        
        return path
    
    def update_path(self, student_id: int,
                   current_mastery: Dict[str, float]) -> List[Dict]:
        """Update learning path based on latest performance"""
        current_path = self.student_paths.get(student_id, [])
        
        adapted_path = self.path_generator.adapt_path(
            current_path, current_mastery
        )
        
        self.student_paths[student_id] = adapted_path
        self.path_history[student_id].append(adapted_path.copy())
        
        return adapted_path
    
    def get_student_path(self, student_id: int) -> List[Dict]:
        """Get current learning path for student"""
        return self.student_paths.get(student_id, [])


if __name__ == '__main__':
    # Example usage
    concepts = ['Concept_1', 'Concept_2', 'Concept_3', 'Concept_4', 'Concept_5']
    
    difficulties = {
        'Concept_1': 0.3,
        'Concept_2': 0.5,
        'Concept_3': 0.4,
        'Concept_4': 0.7,
        'Concept_5': 0.6
    }
    
    prerequisites = {
        'Concept_1': [],
        'Concept_2': ['Concept_1'],
        'Concept_3': ['Concept_1'],
        'Concept_4': ['Concept_2', 'Concept_3'],
        'Concept_5': ['Concept_2']
    }
    
    generator = LearningPathGenerator(concepts, difficulties, prerequisites)
    
    # Student knowledge state
    student_knowledge = {
        'Concept_1': 0.8,
        'Concept_2': 0.4,
        'Concept_3': 0.2,
        'Concept_4': 0.1,
        'Concept_5': 0.3
    }
    
    # Generate path
    path = generator.generate_path(
        student_knowledge,
        weak_concepts=['Concept_3', 'Concept_4'],
        learning_preference='balanced'
    )
    
    print("Generated Learning Path:")
    for node in path:
        print(f"  {node['position']}. {node['concept']}")
        print(f"     Difficulty: {node['difficulty']:.2f}")
        print(f"     Current Mastery: {node['current_mastery']:.2f}")
        print(f"     Bloom Level: {node['bloom_level']}")
        print(f"     Estimated Time: {node['estimated_time']} min")
