"""
MA206 Final Review Autograder
A Streamlit application for automatic grading of MA206 review problems
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

# Page configuration
st.set_page_config(
    page_title="MA206 Review Autograder",
    page_icon="📊",
    layout="wide"
)

# Load answer key
@st.cache_data
def load_answers():
    """Load the answer key from CSV"""
    try:
        return pd.read_csv('MA206_Review_Answers.csv')
    except FileNotFoundError:
        st.error("Answer key file not found. Please ensure MA206_Review_Answers.csv is in the same directory.")
        return None

answers_df = load_answers()

# Section mapping
SECTIONS = {
    'Section 1: Foundational Concepts': ['1.1a', '1.1b', '1.1c', '1.2a', '1.2b', '1.3a', '1.3b', '1.3c'],
    'Section 2: Parameters & Sampling': ['2.1a', '2.1b', '2.1c', '2.2a', '2.2b', '2.2c'],
    'Section 3: Probability Concepts': ['3.1a', '3.1b', '3.1c', '3.2a', '3.2b', '3.2c', '3.3.1', '3.3.2', '3.3.3', '3.3.4', '3.3.5'],
    'Section 4: Selecting Tests': ['4.1', '4.2', '4.3', '4.4', '4.5', '4.6'],
    'Section 5: One-Proportion z-Test': ['5a', '5b', '5c', '5d', '5e', '5f', '5g', '5h', '5i'],
    'Section 6: Two-Sample t-Test': ['6a', '6b', '6c', '6d', '6e', '6f', '6g', '6h', '6i', '6j'],
    'Section 7: Paired t-Test': ['7a', '7b_H0', '7b_Ha', '7c', '7d', '7e', '7f'],
    'Section 8: Simple Linear Regression': ['8a', '8b', '8c', '8d', '8e', '8f'],
    'Section 9: Multiple Regression': ['9a', '9b', '9c', '9d', '10a', '10b'],
    'Section 10: Confounding Variables': ['11a', '11b', '11c'],
    'Section 11: Bayes Theorem': ['12a', '12b', '12c'],
    'Section 12: Discrete Random Variables': ['13a', '13b', '13c', '13d', '13e', '13f', '14a', '14b', '14c'],
    'Section 13: Continuous Random Variables': ['15a', '15b', '15c', '15d', '16a', '16b', '16c'],
    'Section 14: Mixed Practice': ['17a', '17b', '17c', '17d', '18a', '18b', '18c', '19a', '19b']
}

def grade_numeric_answer(student_answer: float, correct_answer: str, tolerance: float = 0.01) -> bool:
    """
    Grade a numeric answer with tolerance for rounding
    
    Args:
        student_answer: The student's numeric answer
        correct_answer: The correct answer as string
        tolerance: Acceptable difference for rounding errors
    
    Returns:
        True if answer is correct within tolerance
    """
    try:
        correct_val = float(correct_answer)
        return abs(float(student_answer) - correct_val) < tolerance
    except (ValueError, TypeError):
        return False

def grade_text_answer(student_answer: str, correct_answer: str, alternatives: str = None) -> bool:
    """
    Grade a text answer allowing for common variations
    
    Args:
        student_answer: The student's text answer
        correct_answer: The primary correct answer
        alternatives: Pipe-separated alternative acceptable answers
    
    Returns:
        True if answer matches correct answer or acceptable alternative
    """
    if not student_answer:
        return False
    
    # Normalize student answer
    student_normalized = str(student_answer).lower().strip()
    correct_normalized = str(correct_answer).lower().strip()
    
    # Check primary answer
    if student_normalized == correct_normalized:
        return True
    
    # Check alternatives
    if pd.notna(alternatives):
        alt_list = [alt.strip().lower() for alt in str(alternatives).split('|')]
        return any(student_normalized == alt for alt in alt_list)
    
    return False

def get_question_data(problem_id: str) -> Dict[str, Any]:
    """Retrieve question data from answer key"""
    if answers_df is None:
        return None
    
    question = answers_df[answers_df['problem_id'] == problem_id]
    if len(question) == 0:
        return None
    
    return question.iloc[0].to_dict()

def render_question_input(problem_id: str, question_data: Dict[str, Any]) -> Any:
    """
    Render appropriate input widget based on answer type
    
    Args:
        problem_id: Unique problem identifier
        question_data: Dictionary containing question information
    
    Returns:
        Student's answer
    """
    st.markdown(f"**Problem {problem_id}:** {question_data['question_part']}")
    
    answer_type = question_data['answer_type']
    
    if answer_type == 'numeric':
        answer = st.number_input(
            "Your answer:",
            key=f"input_{problem_id}",
            format="%.3f",
            step=0.001
        )
    elif answer_type == 'text':
        answer = st.text_input(
            "Your answer:",
            key=f"input_{problem_id}"
        )
    else:
        answer = st.text_input(
            "Your answer:",
            key=f"input_{problem_id}"
        )
    
    return answer

def grade_section(section_name: str, student_answers: Dict[str, Any]) -> Tuple[int, int, list]:
    """
    Grade all answers in a section
    
    Args:
        section_name: Name of the section to grade
        student_answers: Dictionary of student answers by problem_id
    
    Returns:
        Tuple of (earned_points, total_points, results_list)
    """
    problem_ids = SECTIONS[section_name]
    
    total_points = 0
    earned_points = 0
    results = []
    
    for problem_id in problem_ids:
        question_data = get_question_data(problem_id)
        if question_data is None:
            continue
        
        student_answer = student_answers.get(problem_id)
        if student_answer is None:
            continue
        
        points = question_data['points']
        total_points += points
        
        # Grade the answer
        is_correct = False
        if question_data['answer_type'] == 'numeric':
            is_correct = grade_numeric_answer(
                student_answer,
                question_data['correct_answer']
            )
        else:
            is_correct = grade_text_answer(
                student_answer,
                question_data['correct_answer'],
                question_data['alternative_answers']
            )
        
        if is_correct:
            earned_points += points
        
        results.append({
            'problem_id': problem_id,
            'question': question_data['question_part'],
            'student_answer': student_answer,
            'correct': is_correct,
            'points': points,
            'correct_answer': question_data['correct_answer']
        })
    
    return earned_points, total_points, results

# Main app
def main():
    st.title("📊 MA206 Final Exam Review Autograder")
    st.markdown("---")
    
    if answers_df is None:
        st.stop()
    
    # Sidebar
    st.sidebar.title("Navigation")
    selected_section = st.sidebar.selectbox(
        "Choose a section:",
        list(SECTIONS.keys())
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Instructions")
    st.sidebar.markdown("""
    1. Select a section from the dropdown
    2. Answer all questions
    3. Click 'Grade My Answers'
    4. Review your results
    """)
    
    st.sidebar.markdown("---")
    show_answers = st.sidebar.checkbox("Show correct answers after grading")
    
    # Main content
    st.header(selected_section)
    st.markdown("Answer the following questions. Round numeric answers to **3 significant digits**.")
    st.markdown("---")
    
    # Initialize session state for answers
    if 'student_answers' not in st.session_state:
        st.session_state.student_answers = {}
    
    # Display questions
    problem_ids = SECTIONS[selected_section]
    
    for i, problem_id in enumerate(problem_ids):
        question_data = get_question_data(problem_id)
        if question_data is None:
            st.warning(f"Question data not found for {problem_id}")
            continue
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                answer = render_question_input(problem_id, question_data)
                st.session_state.student_answers[problem_id] = answer
            with col2:
                st.markdown(f"<div style='padding-top: 30px;'>({question_data['points']} pts)</div>", 
                           unsafe_allow_html=True)
        
        if i < len(problem_ids) - 1:
            st.markdown("---")
    
    # Grade button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("📝 Grade My Answers", type="primary"):
            st.session_state.graded = True
    
    with col2:
        if st.button("🔄 Clear Answers"):
            st.session_state.student_answers = {}
            st.session_state.graded = False
            st.rerun()
    
    # Display results
    if st.session_state.get('graded', False):
        st.markdown("---")
        st.header("📊 Results")
        
        earned, total, results = grade_section(
            selected_section,
            st.session_state.student_answers
        )
        
        # Overall score
        percentage = (earned / total * 100) if total > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Points Earned", f"{earned}/{total}")
        with col2:
            st.metric("Percentage", f"{percentage:.1f}%")
        with col3:
            if percentage >= 90:
                st.success("Excellent! 🎉")
            elif percentage >= 80:
                st.info("Good job! 👍")
            elif percentage >= 70:
                st.warning("Keep practicing 📚")
            else:
                st.error("More review needed 💪")
        
        st.markdown("---")
        
        # Detailed results
        st.subheader("Detailed Results")
        
        correct_count = sum(1 for r in results if r['correct'])
        st.write(f"Correct answers: {correct_count}/{len(results)}")
        
        for result in results:
            with st.expander(
                f"{'✅' if result['correct'] else '❌'} Problem {result['problem_id']} "
                f"({'Correct' if result['correct'] else 'Incorrect'}) - {result['points']} pts"
            ):
                st.markdown(f"**Question:** {result['question']}")
                st.markdown(f"**Your answer:** {result['student_answer']}")
                
                if not result['correct'] and show_answers:
                    st.markdown(f"**Correct answer:** {result['correct_answer']}")
                elif result['correct']:
                    st.success("Great job! This answer is correct.")

if __name__ == "__main__":
    main()
