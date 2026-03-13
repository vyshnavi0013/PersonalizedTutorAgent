"""
Structured Learning Flow - Guides students through topics with Explanation → Examples → Quiz
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from src.curriculum import Curriculum, Topic
from src.learning_content import LearningContentGenerator

logger = logging.getLogger(__name__)

@dataclass
class TopicProgress:
    """Tracks progress through a single topic"""
    topic_id: str
    topic_name: str
    status: str  # not_started, explanation_viewed, examples_viewed, quiz_offered, completed
    quiz_taken: bool = False
    quiz_score: Optional[float] = None
    explanation_content: Optional[str] = None
    examples_content: Optional[str] = None
    
@dataclass
class StructuredLearningSession:
    """Represents a complete structured learning session"""
    student_level: str  # beginner, intermediate, advanced
    subject: str
    topics: List[Topic] = field(default_factory=list)
    current_topic_index: int = 0
    topic_progress: Dict[str, TopicProgress] = field(default_factory=dict)
    completed_topics: int = 0
    
    def get_current_topic(self) -> Optional[Topic]:
        """Get the current topic"""
        if self.current_topic_index < len(self.topics):
            return self.topics[self.current_topic_index]
        return None
    
    def move_to_next_topic(self):
        """Move to the next topic"""
        if self.current_topic_index < len(self.topics) - 1:
            current_topic = self.get_current_topic()
            if current_topic and current_topic.id in self.topic_progress:
                self.topic_progress[current_topic.id].status = "completed"
            self.current_topic_index += 1
            self.completed_topics += 1
    
    def is_completed(self) -> bool:
        """Check if all topics are completed"""
        return self.current_topic_index >= len(self.topics)
    
    def get_progress_percentage(self) -> float:
        """Get completion percentage"""
        if not self.topics:
            return 0
        return (self.completed_topics / len(self.topics)) * 100

class StructuredLearningManager:
    """Manages structured learning sessions"""
    
    def __init__(self, content_generator: LearningContentGenerator):
        self.content_generator = content_generator
        self.logger = logging.getLogger(__name__)
    
    def create_session(self, subject: str, student_level: str) -> StructuredLearningSession:
        """Create a new structured learning session"""
        topics = Curriculum.get_topics_for_subject_level(subject, student_level)
        
        session = StructuredLearningSession(
            student_level=student_level,
            subject=subject,
            topics=topics,
            current_topic_index=0,
            completed_topics=0
        )
        
        # Initialize topic progress
        for topic in topics:
            session.topic_progress[topic.id] = TopicProgress(
                topic_id=topic.id,
                topic_name=topic.name,
                status="not_started"
            )
        
        return session
    
    def load_topic_explanation(self, session: StructuredLearningSession) -> Dict:
        """Load explanation for current topic"""
        current_topic = session.get_current_topic()
        if not current_topic:
            return {"error": "No current topic"}
        
        try:
            # Generate explanation for the topic
            explanation = self.content_generator.generate_concept_explanation(
                concept=current_topic.name,
                student_level=session.student_level,
                mastery_level=0.5
            )
            
            # Update session
            if current_topic.id in session.topic_progress:
                session.topic_progress[current_topic.id].explanation_content = explanation
                session.topic_progress[current_topic.id].status = "explanation_viewed"
            
            return {
                "topic_id": current_topic.id,
                "topic_name": current_topic.name,
                "topic_description": current_topic.description,
                "explanation": explanation,
                "level": session.student_level
            }
        except Exception as e:
            self.logger.error(f"Error loading explanation: {e}")
            return {"error": str(e)}
    
    def load_topic_examples(self, session: StructuredLearningSession) -> Dict:
        """Load examples for current topic"""
        current_topic = session.get_current_topic()
        if not current_topic:
            return {"error": "No current topic"}
        
        try:
            # Generate examples for the topic using the public method
            material = self.content_generator.generate_learning_material(
                concept=current_topic.name,
                material_type="example",
                student_level=session.student_level
            )
            
            # Update session
            if current_topic.id in session.topic_progress:
                session.topic_progress[current_topic.id].examples_content = material.content
                session.topic_progress[current_topic.id].status = "examples_viewed"
            
            return {
                "topic_id": current_topic.id,
                "topic_name": current_topic.name,
                "examples": material.content,
                "level": session.student_level
            }
        except Exception as e:
            self.logger.error(f"Error loading examples: {e}")
            return {"error": str(e)}
    
    def record_quiz_completion(self, session: StructuredLearningSession, 
                               quiz_taken: bool, score: Optional[float] = None):
        """Record that student took or skipped quiz"""
        current_topic = session.get_current_topic()
        if not current_topic:
            return
        
        if current_topic.id in session.topic_progress:
            session.topic_progress[current_topic.id].quiz_taken = quiz_taken
            if quiz_taken and score is not None:
                session.topic_progress[current_topic.id].quiz_score = score
            session.topic_progress[current_topic.id].status = "quiz_offered"
    
    def get_session_summary(self, session: StructuredLearningSession) -> Dict:
        """Get summary of learning session"""
        completed = sum(1 for p in session.topic_progress.values() 
                       if p.status == "completed")
        quizzes_taken = sum(1 for p in session.topic_progress.values() 
                           if p.quiz_taken)
        
        return {
            "total_topics": len(session.topics),
            "completed_topics": completed,
            "progress_percentage": session.get_progress_percentage(),
            "quizzes_taken": quizzes_taken,
            "average_quiz_score": self._calculate_average_score(session)
        }
    
    def _calculate_average_score(self, session: StructuredLearningSession) -> float:
        """Calculate average quiz score"""
        scores = [p.quiz_score for p in session.topic_progress.values() 
                 if p.quiz_score is not None]
        if not scores:
            return 0
        return sum(scores) / len(scores)
