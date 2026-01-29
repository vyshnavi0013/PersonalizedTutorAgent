"""
Main Runner Script for Personalized Tutor Agent
Generates synthetic data and runs evaluation pipeline
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data'))

from data.generate_synthetic_data import SyntheticDatasetGenerator, save_datasets, get_dataset_statistics
from src.learner_profiling import LearnerProfileManager
from src.knowledge_tracing import SimplifiedDKT, KnowledgeTracingEvaluator
from src.learning_path import LearningPathGenerator, AdaptivePathManager
from src.adaptive_quiz import AdaptiveQuizEngine, QuestionBank
from src.tutor_agent import PersonalizedTutorAgent
from src.evaluation import (
    LearningEffectivenessEvaluator,
    SystemPerformanceAnalyzer,
    ResultsVisualizer,
    EvaluationReport
)


def run_data_generation():
    """Generate synthetic dataset"""
    print("\n" + "="*70)
    print("STEP 1: SYNTHETIC DATA GENERATION")
    print("="*70)
    
    print("\n📊 Generating synthetic dataset...")
    generator = SyntheticDatasetGenerator(
        n_students=50,
        n_concepts=8,
        n_questions=80,
        seed=42
    )
    
    qbank, interactions = generator.generate_complete_dataset(
        n_interactions_per_student=60
    )
    
    print("\n✓ Dataset generated successfully!")
    
    # Save datasets
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    save_datasets(qbank, interactions, data_dir)
    
    # Print statistics
    get_dataset_statistics(qbank, interactions)
    
    return qbank, interactions


def run_learner_profiling(interactions_df):
    """Initialize and run learner profiling"""
    print("\n" + "="*70)
    print("STEP 2: LEARNER PROFILING")
    print("="*70)
    
    concepts = interactions_df['concept'].unique().tolist()
    manager = LearnerProfileManager(concepts)
    
    print(f"\n📚 Building profiles for {interactions_df['student_id'].nunique()} students...")
    manager.update_from_interactions(interactions_df)
    
    print("✓ Learner profiles created!")
    
    # Display summary
    summary = manager.get_learner_profiles_summary()
    print("\n📊 Learner Profiles Summary:")
    print(summary.head(10))
    
    return manager


def run_knowledge_tracing(interactions_df, concepts):
    """Initialize and evaluate knowledge tracing"""
    print("\n" + "="*70)
    print("STEP 3: KNOWLEDGE TRACING (SIMPLIFIED DKT)")
    print("="*70)
    
    print("\n🧠 Initializing Simplified Deep Knowledge Tracing...")
    dkt = SimplifiedDKT(concepts, learning_rate=0.1, forget_rate=0.05)
    
    print("✓ DKT model initialized!")
    
    # Evaluate DKT
    print("\n📈 Evaluating DKT prediction accuracy...")
    dkt_accuracy = SystemPerformanceAnalyzer.evaluate_dkt_accuracy(
        dkt, interactions_df, lookahead=1
    )
    
    print(f"✓ 1-step prediction accuracy: {dkt_accuracy:.1%}")
    
    # Example: Trace a specific student
    sample_student = 1
    trajectory, final_knowledge = dkt.trace_student(interactions_df, sample_student)
    
    print(f"\n📊 Knowledge trajectory for student {sample_student}:")
    for i, step in enumerate(trajectory[-5:]):  # Show last 5 steps
        print(f"   Step {len(trajectory)-4+i}: {step['concept']} -> "
              f"{step['knowledge_after']:.2f} (Correct: {step['is_correct']})")
    
    return dkt


def run_learning_path_generation(concepts, interactions_df, profile_manager):
    """Generate learning paths"""
    print("\n" + "="*70)
    print("STEP 4: LEARNING PATH GENERATION")
    print("="*70)
    
    print("\n🛤️ Initializing learning path generator...")
    
    # Calculate concept difficulties from data
    concept_difficulty = {}
    for concept in concepts:
        concept_data = interactions_df[interactions_df['concept'] == concept]
        error_rate = 1 - concept_data['score'].mean()
        concept_difficulty[concept] = np.clip(error_rate, 0.2, 0.8)
    
    path_gen = LearningPathGenerator(concepts, concept_difficulty=concept_difficulty)
    path_manager = AdaptivePathManager(path_gen)
    
    print("✓ Learning path generator initialized!")
    
    # Generate paths for sample students
    print("\n📚 Generating personalized learning paths for sample students...")
    
    for student_id in [1, 2, 3]:
        profile = profile_manager.get_or_create_profile(student_id)
        knowledge = profile.get_knowledge_state_vector()
        weak_concepts = profile.get_weak_concepts(n=3)
        
        path = path_manager.create_initial_path(student_id, knowledge, weak_concepts)
        
        print(f"\n   Student {student_id} Learning Path:")
        for node in path[:3]:  # Show first 3
            print(f"      {node['position']}. {node['concept']} "
                  f"(Bloom: {node['bloom_level']}, "
                  f"Mastery: {node['current_mastery']:.0%})")
    
    return path_manager


def run_adaptive_quiz(qbank_df):
    """Initialize adaptive quiz engine"""
    print("\n" + "="*70)
    print("STEP 5: ADAPTIVE QUIZ ENGINE")
    print("="*70)
    
    print("\n📝 Initializing adaptive quiz engine...")
    qbank = QuestionBank(qbank_df)
    quiz_engine = AdaptiveQuizEngine(qbank, target_accuracy=0.65)
    
    print("✓ Quiz engine initialized!")
    print(f"   Total questions in bank: {len(qbank.questions)}")
    
    # Simulate a quiz session
    print("\n🎮 Simulating adaptive quiz session...")
    quiz_engine.start_new_quiz()
    
    # Student mastery for simulation
    student_mastery = {
        concept: np.random.uniform(0.3, 0.8)
        for concept in qbank_df['concept'].unique()
    }
    
    for i in range(5):  # 5 question quiz
        concept = list(student_mastery.keys())[i % len(student_mastery)]
        previous_correct = quiz_engine.responses[-1]['is_correct'] if quiz_engine.responses else None
        
        question = quiz_engine.select_next_question(
            student_id=1,
            concept=concept,
            student_mastery=student_mastery[concept],
            previous_correct=previous_correct
        )
        
        # Simulate answer
        is_correct = np.random.binomial(1, 0.65)
        quiz_engine.record_response(question.question_id, 1, is_correct, 45)
    
    stats = quiz_engine.get_quiz_statistics()
    print(f"\n   Quiz Summary:")
    print(f"      Questions: {stats['total_questions']}")
    print(f"      Accuracy: {stats['accuracy']:.1%}")
    
    return quiz_engine


def run_tutor_agent():
    """Initialize tutor agent"""
    print("\n" + "="*70)
    print("STEP 6: PERSONALIZED TUTOR AGENT")
    print("="*70)
    
    print("\n🤖 Initializing personalized tutor agent...")
    tutor = PersonalizedTutorAgent()
    print("✓ Tutor agent initialized!")
    
    # Generate sample feedback
    print("\n💬 Sample Tutor Feedback:")
    
    feedback = tutor.feedback_gen.generate_immediate_feedback(
        is_correct=True,
        concept='Concept_1',
        difficulty='Medium',
        time_spent=45,
        estimated_time=30
    )
    print(f"   Immediate feedback (correct): {feedback}")
    
    hint = tutor.feedback_gen.generate_hint('Concept_1', hint_level=1)
    print(f"   Hint: {hint}")
    
    return tutor


def run_evaluation(interactions_df, profile_manager, dkt, path_manager, quiz_engine):
    """Run comprehensive evaluation"""
    print("\n" + "="*70)
    print("STEP 7: COMPREHENSIVE EVALUATION")
    print("="*70)
    
    print("\n📊 Evaluating system performance...")
    
    # Learning effectiveness
    evaluator = LearningEffectivenessEvaluator()
    
    # Calculate learning gains
    learner_improvements = []
    for student_id in interactions_df['student_id'].unique()[:10]:
        improvement = evaluator.measure_improvement_rate(interactions_df, student_id)
        learner_improvements.append(improvement)
    
    avg_improvement = np.mean(learner_improvements)
    print(f"\n✓ Average Learning Improvement Rate: {avg_improvement:.4f}")
    
    # Generate report
    print("\n📄 Generating evaluation report...")
    
    report = EvaluationReport.generate_report(
        interactions_df,
        profile_manager.profiles,
        dkt,
        path_manager.student_paths,
        output_file='reports/evaluation_report.txt'
    )
    
    print("✓ Evaluation report generated!")
    print("\n" + "="*70)
    print(report)
    print("="*70)
    
    # Generate visualizations
    print("\n🎨 Generating visualizations...")
    os.makedirs('reports', exist_ok=True)
    
    visualizer = ResultsVisualizer()
    visualizer.plot_learning_curves(interactions_df, save_path='reports/learning_curves.png')
    print("✓ Learning curves saved: reports/learning_curves.png")
    
    return report


def main():
    """Main pipeline"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  PERSONALIZED TUTOR AGENT - COMPLETE PIPELINE  ".center(68) + "║")
    print("║" + "  IIT/NIT Research-Aligned Project  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        # Step 1: Data Generation
        qbank_df, interactions_df = run_data_generation()
        concepts = interactions_df['concept'].unique().tolist()
        
        # Step 2: Learner Profiling
        profile_manager = run_learner_profiling(interactions_df)
        
        # Step 3: Knowledge Tracing
        dkt = run_knowledge_tracing(interactions_df, concepts)
        
        # Step 4: Learning Path Generation
        path_manager = run_learning_path_generation(concepts, interactions_df, profile_manager)
        
        # Step 5: Adaptive Quiz
        quiz_engine = run_adaptive_quiz(qbank_df)
        
        # Step 6: Tutor Agent
        tutor = run_tutor_agent()
        
        # Step 7: Evaluation
        report = run_evaluation(interactions_df, profile_manager, dkt, path_manager, quiz_engine)
        
        print("\n" + "="*70)
        print("✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\n📁 Output Files Generated:")
        print("   • data/student_interactions.csv - Student interaction logs")
        print("   • data/question_bank.csv - Question bank")
        print("   • reports/evaluation_report.txt - Evaluation report")
        print("   • reports/learning_curves.png - Learning curves visualization")
        print("\n🚀 To run Streamlit app:")
        print("   streamlit run app.py")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
