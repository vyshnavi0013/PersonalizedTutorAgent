"""
Learning Content Generator
Generates personalized learning materials and real-time recommendations using Groq AI
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LearningMaterial:
    """Represents a learning material item"""
    title: str
    content: str
    concept: str
    difficulty: str
    duration_minutes: int
    material_type: str  # explanation, example, practice, visualization


@dataclass
class LearningRecommendation:
    """Represents a learning recommendation"""
    concept: str
    reason: str
    suggested_material: str
    priority: float  # 0-1, higher = more important
    estimated_time: int  # minutes


class LearningContentGenerator:
    """
    Generates personalized learning content using Groq AI
    Provides:
    - Concept explanations tailored to student level
    - Real-time recommendations based on performance
    - Learning path with structured progression
    """

    def __init__(self):
        """Initialize learning content generator with Groq AI"""
        try:
            from src.groq_ai import GroqAITutor
            self.groq_ai = GroqAITutor()
            logger.info("✅ LearningContentGenerator initialized with Groq AI")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Groq AI: {e}")
            raise

    def generate_concept_explanation(self,
                                    concept: str,
                                    student_level: str = "beginner",
                                    mastery_level: float = 0.0) -> str:
        """
        Generate AI-powered explanation for a concept

        Args:
            concept: Concept to explain
            student_level: beginner, intermediate, or advanced
            mastery_level: Current mastery (0-1)

        Returns:
            AI-generated explanation
        """
        prompt = f"""
        Provide a clear, engaging {student_level}-level explanation of the concept: "{concept}"
        
        Guidelines:
        - Keep it concise (2-3 paragraphs)
        - Use real-world examples
        - Include one practice tip
        - Adapt complexity to {student_level} level
        - If mastery is low ({mastery_level}), include foundational concepts
        
        Current mastery level: {mastery_level:.1%}
        Focus on: {['fundamentals', 'application', 'advanced topics'][int(mastery_level * 2)]}
        """

        try:
            response = self.groq_ai.client.chat.completions.create(
                model=self.groq_ai.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            # Return comprehensive fallback content
            level_desc = {
                "beginner": "the fundamentals and basic concepts",
                "intermediate": "the intermediate concepts and applications", 
                "advanced": "advanced concepts and complex applications"
            }.get(student_level, "the key concepts")
            
            return f"""
            ## Understanding {concept.title()}
            
            **What is {concept}?**
            
            {concept.title()} is a fundamental concept that helps us understand {level_desc}. 
            It forms the basis for more advanced topics and has many practical applications.
            
            **Key Ideas:**
            - {concept} involves understanding core principles
            - It applies to real-world situations
            - Building a strong foundation here helps with advanced topics
            
            **Why It Matters:**
            - Understanding {concept} strengthens your problem-solving skills
            - You'll encounter this concept across many different areas
            - Mastering this builds confidence for future learning
            
            **Real-World Application:**
            {concept} appears everywhere - from everyday situations to professional work. 
            Taking time to understand it deeply will pay dividends later.
            
            **Tip for Learning:**
            Focus on understanding the "why" behind {concept}, not just the "how". 
            When you understand the reasoning, everything else becomes easier.
            
            *Note: Detailed AI-generated content will be available once the AI service is fully connected.*
            """

    def generate_learning_material(self,
                                  concept: str,
                                  material_type: str = "explanation",
                                  student_level: str = "beginner") -> LearningMaterial:
        """
        Generate learning material for a concept

        Args:
            concept: Concept to create material for
            material_type: explanation, example, practice, visualization
            student_level: beginner, intermediate, advanced

        Returns:
            LearningMaterial object
        """
        if material_type == "explanation":
            content = self.generate_concept_explanation(concept, student_level)
            duration = 10
        elif material_type == "example":
            content = self._generate_examples(concept, student_level)
            duration = 8
        elif material_type == "practice":
            content = self._generate_practice_guide(concept, student_level)
            duration = 15
        else:  # visualization
            content = self._generate_visualization_guide(concept, student_level)
            duration = 12

        return LearningMaterial(
            title=f"{material_type.capitalize()}: {concept}",
            content=content,
            concept=concept,
            difficulty=student_level,
            duration_minutes=duration,
            material_type=material_type
        )

    def _generate_examples(self, concept: str, level: str) -> str:
        """Generate practical examples for a concept"""
        prompt = f"""
        Provide 2-3 practical {level}-level examples for: {concept}
        
        Format:
        Example 1: [Scenario]
        - Step 1: [Action]
        - Step 2: [Action]
        - Result: [Outcome]
        
        (Repeat for 2-3 examples)
        """
        try:
            response = self.groq_ai.client.chat.completions.create(
                model=self.groq_ai.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=400
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating examples: {e}")
            # Return fallback content instead of just "unavailable"
            return f"""
            **Real-World Examples for {concept}:**
            
            Example 1: Practical Application
            - Understanding the core concept
            - Applying in real scenarios
            - Observing the results
            
            Example 2: Common Use Cases
            - Identifying where {concept} appears
            - Breaking down the components
            - Seeing the pattern
            
            Example 3: Advanced Application
            - Building on basic understanding
            - Combining multiple concepts
            - Creating complex solutions
            
            *Note: Detailed examples will be available when AI service is connected.*
            """

    def _generate_practice_guide(self, concept: str, level: str) -> str:
        """Generate practice guide for a concept"""
        prompt = f"""
        Create a {level}-level practice guide for: {concept}
        
        Include:
        1. Warm-up exercise (easy)
        2. Main practice problem (medium)
        3. Challenge problem (hard)
        
        For each: provide the problem and hint (not full solution)
        """
        try:
            response = self.groq_ai.client.chat.completions.create(
                model=self.groq_ai.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating practice guide: {e}")
            # Return fallback content
            return f"""
            **Practice Guide for {concept}:**
            
            **Warm-up Exercise:**
            - Start with a basic question about {concept}
            - Hint: Think about the fundamentals
            
            **Main Problem:**
            - A medium-difficulty problem that requires applying {concept}
            - Hint: Break the problem into smaller parts
            
            **Challenge Problem:**
            - An advanced problem that combines multiple concepts
            - Hint: Think creatively about different approaches
            
            *Note: Detailed practice problems will be available when AI service is connected.*
            """

    def _generate_visualization_guide(self, concept: str, level: str) -> str:
        """Generate visualization guidance for a concept"""
        prompt = f"""
        Describe how to visualize the concept: {concept}
        
        Include:
        1. What to draw/visualize
        2. Key elements to highlight
        3. Common misconceptions to avoid
        4. How visualization helps understanding
        
        Make it actionable for a {level}-level student
        """
        try:
            response = self.groq_ai.client.chat.completions.create(
                model=self.groq_ai.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=400
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating visualization guide: {e}")
            # Return fallback content
            return f"""
            **Visualization Guide for {concept}:**
            
            **What to Draw:**
            - Create a visual representation of {concept}
            - Use diagrams, graphs, or sketches
            
            **Key Elements to Highlight:**
            - The main components of {concept}
            - How they relate to each other
            - Important properties and characteristics
            
            **Common Misconceptions:**
            - Avoid thinking of {concept} as...
            - Instead, focus on...
            
            **How Visualization Helps:**
            - Seeing the bigger picture
            - Understanding relationships
            - Building intuition
            
            *Note: Detailed visualizations will be available when AI service is connected.*
            """

    def generate_real_time_recommendations(self,
                                         course_concepts: List[str],
                                         student_knowledge: Dict[str, float],
                                         recent_performance: Dict[str, float],
                                         student_level: str) -> List[LearningRecommendation]:
        """
        Generate real-time learning recommendations based on performance

        Args:
            course_concepts: Concepts in the course
            student_knowledge: Current mastery for each concept
            recent_performance: Recent accuracy for each concept
            student_level: beginner, intermediate, advanced

        Returns:
            List of ranked recommendations
        """
        recommendations = []

        for concept in course_concepts:
            mastery = student_knowledge.get(concept, 0.0)
            recent_acc = recent_performance.get(concept, 0.5)

            # Calculate priority
            if recent_acc < 0.5:  # Struggling
                priority = 0.95
                reason = "You struggled with this recently - needs review"
            elif mastery < 0.3:  # Not yet proficient
                priority = 0.85
                reason = "You haven't mastered this concept yet"
            elif mastery < 0.7:  # Partial mastery
                priority = 0.6
                reason = "You're making progress - ready for more practice"
            else:  # Mastered
                priority = 0.2
                reason = "Well done! Move to more advanced topics"

            rec = LearningRecommendation(
                concept=concept,
                reason=reason,
                suggested_material=self._suggest_material_type(
                    mastery, recent_acc
                ),
                priority=priority,
                estimated_time=self._estimate_learning_time(
                    mastery, recent_acc
                )
            )
            recommendations.append(rec)

        # Sort by priority (highest first)
        recommendations.sort(key=lambda x: x.priority, reverse=True)
        return recommendations

    def _suggest_material_type(self, mastery: float, recent_acc: float) -> str:
        """Suggest appropriate material type based on performance"""
        if recent_acc < 0.4:
            return "explanation"
        elif mastery < 0.3:
            return "example"
        elif mastery < 0.7:
            return "practice"
        else:
            return "visualization"

    def _estimate_learning_time(self, mastery: float, recent_acc: float) -> int:
        """Estimate learning time needed"""
        if recent_acc < 0.4:
            return 20  # Needs foundational review
        elif mastery < 0.3:
            return 15
        elif mastery < 0.7:
            return 10
        else:
            return 5


class LearningPathOrchestrator:
    """
    Orchestrates the complete learning path experience
    Combines adaptive sequencing with content generation
    """

    def __init__(self):
        """Initialize orchestrator"""
        self.content_gen = LearningContentGenerator()

    def create_personalized_learning_session(self,
                                            course_id: str,
                                            course_concepts: List[str],
                                            student_knowledge: Dict[str, float],
                                            student_level: str,
                                            recent_performance: Dict[str, float]) -> Dict:
        """
        Create a complete personalized learning session

        Args:
            course_id: Selected course
            course_concepts: Concepts to cover
            student_knowledge: Current mastery
            student_level: beginner, intermediate, advanced
            recent_performance: Recent quiz performance

        Returns:
            Complete learning session plan
        """
        # Get real-time recommendations
        recommendations = self.content_gen.generate_real_time_recommendations(
            course_concepts=course_concepts,
            student_knowledge=student_knowledge,
            recent_performance=recent_performance,
            student_level=student_level
        )

        # Build learning session
        session = {
            "course_id": course_id,
            "student_level": student_level,
            "recommendations": recommendations,
            "learning_materials": [],
            "estimated_total_time": 0
        }

        # Generate materials for top 3 recommendations
        for i, rec in enumerate(recommendations[:3]):
            material = self.content_gen.generate_learning_material(
                concept=rec.concept,
                material_type=rec.suggested_material,
                student_level=student_level
            )
            session["learning_materials"].append({
                "order": i + 1,
                "recommendation": rec,
                "material": material
            })
            session["estimated_total_time"] += material.duration_minutes

        return session

    def generate_session_summary(self, session: Dict) -> str:
        """Generate a summary of the learning session"""
        summary = f"""
🎓 **Your Personalized Learning Path**

📚 Level: {session['student_level'].capitalize()}
⏱️ Estimated Time: {session['estimated_total_time']} minutes

**Recommended Learning Sequence:**
"""
        for item in session["learning_materials"]:
            rec = item["recommendation"]
            mat = item["material"]
            summary += f"""
{item['order']}. **{rec.concept.capitalize()}** ({mat.material_type})
   📌 {rec.reason}
   ⏱️ {mat.duration_minutes} minutes
   📖 {mat.suggested_material}
"""
        return summary
