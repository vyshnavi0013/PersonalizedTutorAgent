from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Course:
    """Represents a learning course"""
    id: str
    name: str
    description: str
    difficulty: str  # beginner, intermediate, advanced
    concepts: List[str]
    duration_hours: float
    prerequisites: List[str]

class CourseManager:
    """Manages the course catalog"""

    COURSES = {
        "math-101": Course(
            id="math-101",
            name="Algebra Fundamentals",
            description="Master basic algebraic equations and expressions",
            difficulty="beginner",
            concepts=["algebra"],
            duration_hours=10,
            prerequisites=[]
        ),
        "math-201": Course(
            id="math-201",
            name="Geometry Basics",
            description="Learn the fundamentals of geometry",
            difficulty="intermediate",
            concepts=["geometry"],
            duration_hours=15,
            prerequisites=["math-101"]
        ),
        "math-301": Course(
            id="math-301",
            name="Calculus Introduction",
            description="Introduction to differential and integral calculus",
            difficulty="advanced",
            concepts=["calculus"],
            duration_hours=20,
            prerequisites=["math-201"]
        )
    }

    @classmethod
    def get_courses(cls) -> List[Course]:
        """Retrieve all available courses"""
        return list(cls.COURSES.values())

    @classmethod
    def get_course(cls, course_id: str) -> Course:
        """Retrieve a specific course by ID"""
        return cls.COURSES.get(course_id)

    @classmethod
    def get_prerequisites(cls, course_id: str) -> List[str]:
        """Retrieve prerequisites for a course"""
        course = cls.get_course(course_id)
        return course.prerequisites if course else []