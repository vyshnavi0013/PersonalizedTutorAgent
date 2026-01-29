"""
Personalized Tutor Agent Package
"""

__version__ = "1.0.0"
__author__ = "IIT/NIT Research Project"

from .learner_profiling import LearnerProfile, LearnerProfileManager
from .knowledge_tracing import SimplifiedDKT, KnowledgeTracingEvaluator
from .learning_path import LearningPathGenerator, AdaptivePathManager
from .adaptive_quiz import AdaptiveQuizEngine, QuestionBank
from .tutor_agent import PersonalizedTutorAgent
from .evaluation import LearningEffectivenessEvaluator, SystemPerformanceAnalyzer

__all__ = [
    'LearnerProfile',
    'LearnerProfileManager',
    'SimplifiedDKT',
    'KnowledgeTracingEvaluator',
    'LearningPathGenerator',
    'AdaptivePathManager',
    'AdaptiveQuizEngine',
    'QuestionBank',
    'PersonalizedTutorAgent',
    'LearningEffectivenessEvaluator',
    'SystemPerformanceAnalyzer'
]
