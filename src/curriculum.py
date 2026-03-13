"""
Curriculum - Topics and learning sequences for each subject and level
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Topic:
    """Represents a learning topic"""
    id: str
    name: str
    description: str
    level: str  # beginner, intermediate, advanced
    subject: str
    order: int

class Curriculum:
    """Defines curriculum with topics for each subject and level"""
    
    MATHEMATICS = {
        "beginner": [
            Topic("math_b_01", "Numbers and Basic Operations", "Understanding integers, fractions, and decimals", "beginner", "Mathematics", 1),
            Topic("math_b_02", "Introduction to Algebra", "Variables, expressions, and simple equations", "beginner", "Mathematics", 2),
            Topic("math_b_03", "Linear Equations", "Solving simple linear equations", "beginner", "Mathematics", 3),
            Topic("math_b_04", "Fractions and Decimals", "Working with fractions and decimal numbers", "beginner", "Mathematics", 4),
            Topic("math_b_05", "Percentages", "Understanding and calculating percentages", "beginner", "Mathematics", 5),
            Topic("math_b_06", "Basic Geometry", "Points, lines, angles, and shapes", "beginner", "Mathematics", 6),
            Topic("math_b_07", "Measurement", "Length, area, volume, and units", "beginner", "Mathematics", 7),
            Topic("math_b_08", "Data and Statistics Basics", "Collecting and interpreting data", "beginner", "Mathematics", 8),
            Topic("math_b_09", "Ratios and Proportions", "Understanding ratios and proportional relationships", "beginner", "Mathematics", 9),
            Topic("math_b_10", "Introduction to Exponents", "Powers and exponential notation", "beginner", "Mathematics", 10),
        ],
        "intermediate": [
            Topic("math_i_01", "Quadratic Equations", "Solving equations of the form ax² + bx + c = 0", "intermediate", "Mathematics", 1),
            Topic("math_i_02", "Polynomials", "Working with polynomial expressions and factoring", "intermediate", "Mathematics", 2),
            Topic("math_i_03", "Systems of Equations", "Solving multiple equations simultaneously", "intermediate", "Mathematics", 3),
            Topic("math_i_04", "Functions and Graphs", "Understanding functions and their graphical representations", "intermediate", "Mathematics", 4),
            Topic("math_i_05", "Quadratic Functions", "Properties and graphs of quadratic functions", "intermediate", "Mathematics", 5),
            Topic("math_i_06", "Exponents and Radicals", "Working with powers and roots", "intermediate", "Mathematics", 6),
            Topic("math_i_07", "Rational Expressions", "Simplifying and solving rational equations", "intermediate", "Mathematics", 7),
            Topic("math_i_08", "Trigonometry Basics", "Sine, cosine, and tangent functions", "intermediate", "Mathematics", 8),
            Topic("math_i_09", "Probability Fundamentals", "Basic probability and counting principles", "intermediate", "Mathematics", 9),
            Topic("math_i_10", "Sequences and Series", "Arithmetic and geometric sequences", "intermediate", "Mathematics", 10),
        ],
        "advanced": [
            Topic("math_a_01", "Advanced Algebra", "Complex algebraic manipulations and proofs", "advanced", "Mathematics", 1),
            Topic("math_a_02", "Calculus - Limits", "Understanding limits and continuity", "advanced", "Mathematics", 2),
            Topic("math_a_03", "Derivatives", "Rates of change and differentiation", "advanced", "Mathematics", 3),
            Topic("math_a_04", "Applications of Derivatives", "Optimization and related rates problems", "advanced", "Mathematics", 4),
            Topic("math_a_05", "Integration", "Antiderivatives and integration techniques", "advanced", "Mathematics", 5),
            Topic("math_a_06", "Differential Equations", "Solving and applications of differential equations", "advanced", "Mathematics", 6),
            Topic("math_a_07", "Linear Algebra", "Matrices, vectors, and transformations", "advanced", "Mathematics", 7),
            Topic("math_a_08", "Complex Numbers", "Working with complex numbers and operations", "advanced", "Mathematics", 8),
            Topic("math_a_09", "Multivariable Calculus", "Functions of multiple variables", "advanced", "Mathematics", 9),
            Topic("math_a_10", "Advanced Probability", "Probability distributions and statistics", "advanced", "Mathematics", 10),
        ]
    }
    
    PHYSICS = {
        "beginner": [
            Topic("phys_b_01", "Motion Basics", "Distance, displacement, speed, and velocity", "beginner", "Physics", 1),
            Topic("phys_b_02", "Acceleration and Forces", "Newton's laws of motion", "beginner", "Physics", 2),
            Topic("phys_b_03", "Work and Energy", "Understanding work, kinetic and potential energy", "beginner", "Physics", 3),
            Topic("phys_b_04", "Heat and Temperature", "Temperature scales and heat transfer", "beginner", "Physics", 4),
            Topic("phys_b_05", "Waves Basics", "Wavelength, frequency, and wave properties", "beginner", "Physics", 5),
            Topic("phys_b_06", "Sound", "Properties and behavior of sound waves", "beginner", "Physics", 6),
            Topic("phys_b_07", "Light Fundamentals", "Reflection, refraction, and light properties", "beginner", "Physics", 7),
            Topic("phys_b_08", "Electricity Basics", "Charge, current, and voltage", "beginner", "Physics", 8),
            Topic("phys_b_09", "Magnetism", "Magnetic fields and interactions", "beginner", "Physics", 9),
            Topic("phys_b_10", "Simple Machines", "Levers, pulleys, and mechanical advantage", "beginner", "Physics", 10),
        ],
        "intermediate": [
            Topic("phys_i_01", "Circular Motion", "Centripetal force and angular velocity", "intermediate", "Physics", 1),
            Topic("phys_i_02", "Rotational Dynamics", "Torque, angular momentum, and moment of inertia", "intermediate", "Physics", 2),
            Topic("phys_i_03", "Gravitation", "Newton's law of universal gravitation", "intermediate", "Physics", 3),
            Topic("phys_i_04", "Fluids", "Pressure, buoyancy, and fluid dynamics", "intermediate", "Physics", 4),
            Topic("phys_i_05", "Thermodynamics", "Heat, entropy, and laws of thermodynamics", "intermediate", "Physics", 5),
            Topic("phys_i_06", "Electrostatics", "Electric fields and Coulomb's law", "intermediate", "Physics", 6),
            Topic("phys_i_07", "Magnetism Advanced", "Magnetic fields from currents", "intermediate", "Physics", 7),
            Topic("phys_i_08", "Electromagnetic Waves", "Light as electromagnetic radiation", "intermediate", "Physics", 8),
            Topic("phys_i_09", "Optics", "Lenses, mirrors, and optical instruments", "intermediate", "Physics", 9),
            Topic("phys_i_10", "Modern Physics Intro", "Quantum mechanics and relativity basics", "intermediate", "Physics", 10),
        ],
        "advanced": [
            Topic("phys_a_01", "Classical Mechanics", "Lagrangian and Hamiltonian mechanics", "advanced", "Physics", 1),
            Topic("phys_a_02", "Special Relativity", "Space-time and relativistic mechanics", "advanced", "Physics", 2),
            Topic("phys_a_03", "General Relativity", "Gravitational fields and curved space-time", "advanced", "Physics", 3),
            Topic("phys_a_04", "Quantum Mechanics", "Schrödinger equation and wavefunctions", "advanced", "Physics", 4),
            Topic("phys_a_05", "Atomic Physics", "Atomic structure and quantum numbers", "advanced", "Physics", 5),
            Topic("phys_a_06", "Nuclear Physics", "Nuclear reactions and radioactivity", "advanced", "Physics", 6),
            Topic("phys_a_07", "Particle Physics", "Fundamental particles and interactions", "advanced", "Physics", 7),
            Topic("phys_a_08", "Field Theory", "Classical and quantum field theories", "advanced", "Physics", 8),
            Topic("phys_a_09", "Solid State Physics", "Crystal structures and band theory", "advanced", "Physics", 9),
            Topic("phys_a_10", "Advanced Thermodynamics", "Statistical mechanics and phase transitions", "advanced", "Physics", 10),
        ]
    }
    
    CHEMISTRY = {
        "beginner": [
            Topic("chem_b_01", "Atoms and Elements", "Atomic structure and the periodic table", "beginner", "Chemistry", 1),
            Topic("chem_b_02", "Chemical Bonding", "Ionic and covalent bonds", "beginner", "Chemistry", 2),
            Topic("chem_b_03", "Compounds and Formulas", "Writing and naming chemical compounds", "beginner", "Chemistry", 3),
            Topic("chem_b_04", "States of Matter", "Solids, liquids, gases, and plasmas", "beginner", "Chemistry", 4),
            Topic("chem_b_05", "Mixtures and Solutions", "Mixtures, solutions, and concentration", "beginner", "Chemistry", 5),
            Topic("chem_b_06", "Acids and Bases", "pH scale and acid-base chemistry", "beginner", "Chemistry", 6),
            Topic("chem_b_07", "Chemical Reactions", "Types of chemical reactions", "beginner", "Chemistry", 7),
            Topic("chem_b_08", "Stoichiometry Basics", "Balancing equations and mole calculations", "beginner", "Chemistry", 8),
            Topic("chem_b_09", "Energy in Chemistry", "Exothermic and endothermic reactions", "beginner", "Chemistry", 9),
            Topic("chem_b_10", "Organic Chemistry Intro", "Hydrocarbons and basic organic compounds", "beginner", "Chemistry", 10),
        ],
        "intermediate": [
            Topic("chem_i_01", "Atomic Orbitals", "Quantum numbers and electron configurations", "intermediate", "Chemistry", 1),
            Topic("chem_i_02", "Chemical Bonding Advanced", "Molecular orbital theory", "intermediate", "Chemistry", 2),
            Topic("chem_i_03", "Equilibrium", "Chemical equilibrium and Le Chatelier's principle", "intermediate", "Chemistry", 3),
            Topic("chem_i_04", "Thermochemistry", "Enthalpy and entropy", "intermediate", "Chemistry", 4),
            Topic("chem_i_05", "Kinetics", "Reaction rates and mechanisms", "intermediate", "Chemistry", 5),
            Topic("chem_i_06", "Electrochemistry", "Redox reactions and electrochemical cells", "intermediate", "Chemistry", 6),
            Topic("chem_i_07", "Coordination Chemistry", "Complex ions and coordination compounds", "intermediate", "Chemistry", 7),
            Topic("chem_i_08", "Organic Reactions", "Substitution, elimination, and addition reactions", "intermediate", "Chemistry", 8),
            Topic("chem_i_09", "Spectroscopy Basics", "UV-Vis and IR spectroscopy", "intermediate", "Chemistry", 9),
            Topic("chem_i_10", "Biochemistry Intro", "Amino acids, proteins, and nucleic acids", "intermediate", "Chemistry", 10),
        ],
        "advanced": [
            Topic("chem_a_01", "Quantum Chemistry", "Molecular orbital calculations", "advanced", "Chemistry", 1),
            Topic("chem_a_02", "Advanced Thermodynamics", "Gibbs energy and spontaneity", "advanced", "Chemistry", 2),
            Topic("chem_a_03", "Advanced Kinetics", "Complex reaction mechanisms", "advanced", "Chemistry", 3),
            Topic("chem_a_04", "Advanced Equilibrium", "Multiple equilibria and buffer systems", "advanced", "Chemistry", 4),
            Topic("chem_a_05", "Surface Chemistry", "Catalysis and surface phenomena", "advanced", "Chemistry", 5),
            Topic("chem_a_06", "Polymer Chemistry", "Polymerization and polymer properties", "advanced", "Chemistry", 6),
            Topic("chem_a_07", "Green Chemistry", "Sustainable chemical processes", "advanced", "Chemistry", 7),
            Topic("chem_a_08", "Analytical Chemistry", "Quantitative analysis techniques", "advanced", "Chemistry", 8),
            Topic("chem_a_09", "Inorganic Chemistry", "Transition metals and complex compounds", "advanced", "Chemistry", 9),
            Topic("chem_a_10", "Advanced Organic Synthesis", "Synthetic strategies and named reactions", "advanced", "Chemistry", 10),
        ]
    }
    
    @classmethod
    def get_topics_for_subject_level(cls, subject: str, level: str) -> List[Topic]:
        """Get topics for a specific subject and level"""
        curriculum_map = {
            "Mathematics": cls.MATHEMATICS,
            "Physics": cls.PHYSICS,
            "Chemistry": cls.CHEMISTRY,
        }
        
        if subject not in curriculum_map:
            return []
        
        return curriculum_map[subject].get(level, [])
    
    @classmethod
    def get_topic(cls, topic_id: str) -> Topic:
        """Get a specific topic by ID"""
        for subject_curriculum in [cls.MATHEMATICS, cls.PHYSICS, cls.CHEMISTRY]:
            for level_topics in subject_curriculum.values():
                for topic in level_topics:
                    if topic.id == topic_id:
                        return topic
        return None
