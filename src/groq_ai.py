"""
Groq AI Integration for Personalized Tutor
Provides AI-powered feedback, hints, and explanations using Groq API
"""

import logging
from typing import Dict, List, Optional, Any
import time
from groq import Groq

from .config import get_config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqAITutor:
    """AI-powered tutor using Groq API"""
    
    def __init__(self):
        """Initialize Groq AI tutor with API configuration"""
        self.config = get_config()
        
        try:
            api_key = self.config.get_groq_api_key()
            self.client = Groq(api_key=api_key)
            self.model = self.config.get_groq_model()
            self.timeout = self.config.get_response_timeout()
            self.retry_attempts = self.config.get_retry_attempts()
            self.log_calls = self.config.should_log_ai_calls()
            
            logger.info(f"✅ Groq AI initialized with model: {self.model}")
            
        except ValueError as e:
            logger.error(f"❌ Failed to initialize Groq AI: {e}")
            raise
    
    def _call_groq(self, messages: List[Dict[str, str]], 
                   max_tokens: int = 1024,
                   temperature: float = 0.7) -> str:
        """
        Call Groq API with retry logic
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-2)
            
        Returns:
            AI response text
            
        Raises:
            RuntimeError: If all retry attempts fail
        """
        for attempt in range(self.retry_attempts):
            try:
                if self.log_calls:
                    logger.info(f"🤖 Calling Groq API (attempt {attempt + 1}/{self.retry_attempts})")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    timeout=self.timeout
                )
                
                content = response.choices[0].message.content
                
                if self.log_calls:
                    logger.info(f"✅ Groq API response received ({len(content)} chars)")
                
                return content
                
            except Exception as e:
                logger.warning(f"⚠️ Groq API error (attempt {attempt + 1}): {e}")
                
                if attempt < self.retry_attempts - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ Failed after {self.retry_attempts} attempts")
                    raise RuntimeError(f"Groq API failed after {self.retry_attempts} attempts: {e}")
    
    def generate_immediate_feedback(self, 
                                   is_correct: bool,
                                   student_response: str,
                                   correct_answer: str,
                                   concept: str,
                                   difficulty: str,
                                   mastery_level: float,
                                   time_spent: int,
                                   estimated_time: int) -> str:
        """
        Generate AI-powered immediate feedback
        
        Args:
            is_correct: Whether answer was correct
            student_response: Student's answer
            correct_answer: Correct answer
            concept: Concept being tested
            difficulty: Question difficulty level
            mastery_level: Student's current mastery (0-1)
            time_spent: Time spent on question (seconds)
            estimated_time: Expected time for question (seconds)
            
        Returns:
            Personalized feedback message
        """
        prompt = f"""You are a supportive and encouraging educational tutor. Generate personalized feedback for a student.

Student Profile:
- Concept: {concept}
- Current Mastery Level: {mastery_level:.1%}
- Time Spent: {time_spent} seconds (Expected: {estimated_time} seconds)

Question Info:
- Difficulty: {difficulty}
- Student's Answer: {student_response}
- Correct Answer: {correct_answer}
- Result: {'CORRECT ✓' if is_correct else 'INCORRECT ✗'}

Generate feedback that:
1. Is encouraging and supportive (avoid discouraging language)
2. Acknowledges effort regardless of correctness
3. For correct answers: Praise the achievement and suggest next steps
4. For incorrect answers: Explain why the answer is wrong and provide guidance
5. Is concise (2-3 sentences)
6. Includes a specific learning suggestion

Keep tone positive and motivating."""

        messages = [
            {"role": "system", "content": "You are an expert, supportive educational tutor."},
            {"role": "user", "content": prompt}
        ]
        
        feedback = self._call_groq(messages, max_tokens=256, temperature=0.8)
        
        return feedback.strip()
    
    def generate_hint(self, 
                     concept: str,
                     question: str,
                     student_attempt: str,
                     hint_level: int = 1,
                     attempt_number: int = 1) -> str:
        """
        Generate progressive hints
        
        Args:
            concept: Target concept
            question: The quiz question
            student_attempt: Student's current attempt/response
            hint_level: Level of hint detail (1=minimal, 3=detailed)
            attempt_number: Which attempt is this
            
        Returns:
            Helpful hint text
        """
        hint_descriptions = {
            1: "a very subtle hint that points in the right direction without giving away the answer",
            2: "a more direct hint that explains what approach to use",
            3: "a detailed explanation of the solution approach"
        }
        
        level_desc = hint_descriptions.get(hint_level, hint_descriptions[1])
        
        prompt = f"""You are an educational tutor providing progressive hints to a student.

Concept: {concept}
Question: {question}
Student's Attempt: {student_attempt}
Attempt Number: {attempt_number}
Hint Level: {hint_level} (on scale of 1-3, where 1 is minimal and 3 is detailed)

Provide {level_desc} for this student.

Requirements:
- Do NOT give away the complete answer
- Focus on the learning process, not just the solution
- Be encouraging
- Keep hint concise (1-2 sentences)"""

        messages = [
            {"role": "system", "content": "You are an expert educational tutor skilled at providing progressive hints."},
            {"role": "user", "content": prompt}
        ]
        
        hint = self._call_groq(messages, max_tokens=200, temperature=0.7)
        
        return f"💭 Hint {hint_level}: {hint.strip()}"
    
    def generate_explanation(self, 
                           concept: str,
                           context: Optional[str] = None,
                           detail_level: str = 'basic') -> str:
        """
        Generate concept explanation
        
        Args:
            concept: Concept to explain
            context: Additional context about the student's question
            detail_level: 'basic', 'intermediate', or 'advanced'
            
        Returns:
            Concept explanation
        """
        detail_prompts = {
            'basic': 'Provide a clear, simple explanation suitable for a beginner.',
            'intermediate': 'Provide a moderate-depth explanation with key concepts and connections.',
            'advanced': 'Provide a detailed explanation including advanced applications and implications.'
        }
        
        detail_prompt = detail_prompts.get(detail_level, detail_prompts['basic'])
        
        context_str = f"\nStudent's Question: {context}" if context else ""
        
        prompt = f"""You are an expert educator explaining concepts clearly.

Concept to Explain: {concept}{context_str}

{detail_prompt}

Format your response as:
1. Definition (1 sentence)
2. Key Points (2-3 bullets)
3. Example (practical application)
4. Connection to Learning (how to remember it)

Keep the explanation engaging and easy to understand."""

        messages = [
            {"role": "system", "content": "You are an expert educator skilled at explaining complex concepts clearly."},
            {"role": "user", "content": prompt}
        ]
        
        explanation = self._call_groq(messages, max_tokens=512, temperature=0.7)
        
        return explanation.strip()
    
    def generate_next_steps(self,
                          concept: str,
                          mastery_level: float,
                          weak_areas: List[str],
                          available_concepts: List[str],
                          total_questions: int) -> str:
        """
        Generate personalized learning path recommendation
        
        Args:
            concept: Current concept
            mastery_level: Current mastery level (0-1)
            weak_areas: List of weak concept areas
            available_concepts: List of available next concepts
            total_questions: Total questions completed
            
        Returns:
            Personalized next steps recommendation
        """
        weak_str = ', '.join(weak_areas) if weak_areas else 'None identified'
        available_str = ', '.join(available_concepts) if available_concepts else 'None available'
        
        prompt = f"""You are a personalized learning advisor. Create a specific learning path recommendation.

Current Status:
- Current Concept: {concept}
- Mastery Level: {mastery_level:.1%}
- Questions Completed: {total_questions}
- Weak Areas: {weak_str}
- Available Next Concepts: {available_str}

Provide a personalized recommendation that:
1. Advises whether to continue or move forward based on mastery level
2. Suggests specific next steps (e.g., more practice, review, or new concept)
3. Addresses weak areas strategically
4. Encourages the student

Format as:
📚 Your Personalized Learning Path:
1. [Next action with reasoning]
2. [Step after that]
3. [Long-term suggestion]

Be specific and actionable."""

        messages = [
            {"role": "system", "content": "You are an expert learning advisor creating personalized educational paths."},
            {"role": "user", "content": prompt}
        ]
        
        recommendation = self._call_groq(messages, max_tokens=400, temperature=0.7)
        
        return recommendation.strip()
    
    def generate_motivational_message(self,
                                     mastery_level: float,
                                     total_questions: int,
                                     accuracy: float,
                                     streak: int = 0,
                                     recent_performance: Optional[str] = None) -> str:
        """
        Generate motivational message based on progress
        
        Args:
            mastery_level: Current overall mastery
            total_questions: Total questions attempted
            accuracy: Overall accuracy (0-1)
            streak: Correct answer streak
            recent_performance: Description of recent performance
            
        Returns:
            Motivational message
        """
        performance_context = f"\nRecent Performance: {recent_performance}" if recent_performance else ""
        
        prompt = f"""You are an encouraging educational coach. Create a motivational message for a student.

Progress Metrics:
- Overall Mastery Level: {mastery_level:.1%}
- Questions Completed: {total_questions}
- Overall Accuracy: {accuracy:.1%}
- Current Streak: {streak} correct answers{performance_context}

Create a motivational message that:
1. Celebrates their achievements specifically (use the metrics)
2. Recognizes effort and progress
3. Provides encouragement for next steps
4. Sets a positive, achievable outlook
5. Is personal and genuine (not generic)

Include emoji where appropriate for engagement. Keep it concise but impactful."""

        messages = [
            {"role": "system", "content": "You are an enthusiastic and genuine educational coach who motivates students effectively."},
            {"role": "user", "content": prompt}
        ]
        
        message = self._call_groq(messages, max_tokens=300, temperature=0.9)
        
        return message.strip()
    
    def analyze_error_pattern(self,
                             concept: str,
                             errors: List[str],
                             mastery_level: float) -> str:
        """
        Analyze common error patterns
        
        Args:
            concept: Concept where errors occurred
            errors: List of common errors
            mastery_level: Current mastery level
            
        Returns:
            Error analysis and recommendations
        """
        errors_str = '\n'.join([f"- {error}" for error in errors[:5]])
        
        prompt = f"""You are an expert educational analyst. Analyze error patterns and provide insights.

Concept: {concept}
Student's Mastery Level: {mastery_level:.1%}

Common Errors Made:
{errors_str}

Provide:
1. Root cause analysis (why these errors occur)
2. 2-3 specific misconceptions to address
3. Targeted practice recommendations
4. Preventive strategies for the future

Format as:
📊 Error Analysis:
🎯 Root Cause: [...]
❌ Common Misconceptions: [...]
📋 Recommended Practice: [...]
✨ Prevention Tips: [...]"""

        messages = [
            {"role": "system", "content": "You are an expert educational psychologist analyzing learning errors."},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self._call_groq(messages, max_tokens=500, temperature=0.7)
        
        return analysis.strip()
    
    def generate_quiz_question(self, 
                             concept: str,
                             difficulty: str = "Medium",
                             mastery_level: float = 0.5) -> Dict[str, Any]:
        """
        Generate an AI-created quiz question with correct answer
        
        Args:
            concept: Concept to create question for
            difficulty: Easy/Medium/Hard
            mastery_level: Student's current mastery level (0-1)
            
        Returns:
            Dict with 'question', 'options', 'correct_answer', 'explanation'
        """
        prompt = f"""You are an expert teacher creating a quiz question.

Generate a {difficulty.lower()} quiz question about: {concept}
Student's Mastery Level: {mastery_level:.1%}

IMPORTANT: Create question appropriate for the mastery level and difficulty.

Return ONLY valid JSON (no markdown, no extra text):
{{
    "question": "Clear, concise question text about {concept}",
    "options": [
        "First plausible option",
        "Second plausible option",
        "Third plausible option",
        "Fourth plausible option"
    ],
    "correct_answer": "The correct option (must be one of the four options above)",
    "correct_index": 0,
    "explanation": "Why this answer is correct"
}}

Requirements:
1. question: Clear and specific
2. options: All plausible, only one correct
3. correct_answer: Exact match to one option
4. correct_index: 0-3 position of correct answer in options list
5. explanation: Educational value explaining why answer is correct"""

        messages = [
            {"role": "system", "content": "You are an expert educator creating quiz questions. Always return valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self._call_groq(messages, max_tokens=800, temperature=0.8)
            
            # Parse JSON response
            import json
            
            # Clean up response (remove markdown if present)
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            question_data = json.loads(cleaned.strip())
            
            # Validate structure
            required_keys = ['question', 'options', 'correct_answer', 'correct_index', 'explanation']
            if not all(key in question_data for key in required_keys):
                raise ValueError(f"Missing required keys in response")
            
            # Validate correct_index
            if not isinstance(question_data['correct_index'], int) or question_data['correct_index'] < 0 or question_data['correct_index'] > 3:
                question_data['correct_index'] = 0
            
            return question_data
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            # Return a fallback question
            return {
                "question": f"What is a key aspect of {concept}?",
                "options": [
                    "Implementation and application",
                    "Theoretical foundation",
                    "Practical examples",
                    "Real-world scenarios"
                ],
                "correct_answer": "Practical examples",
                "correct_index": 2,
                "explanation": f"Understanding {concept} requires looking at practical examples to see how concepts apply in real situations."
            }
        except Exception as e:
            logger.error(f"Error generating question: {e}")
            # Return a fallback question
            return {
                "question": f"What is a key aspect of {concept}?",
                "options": [
                    "Implementation and application",
                    "Theoretical foundation",
                    "Practical examples",
                    "Real-world scenarios"
                ],
                "correct_answer": "Practical examples",
                "correct_index": 2,
                "explanation": f"Understanding {concept} requires looking at practical examples to see how concepts apply in real situations."
            }
