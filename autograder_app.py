import streamlit as st
import pandas as pd

st.set_page_config(page_title="MA206 Review", page_icon="📊", layout="wide")

@st.cache_data
def load_questions():
    return pd.read_csv('MA206_Review_Answers.csv')

df = load_questions()

st.title("📊 MA206 Final Exam Review")
st.markdown("**Instructions:** Select the best answer for each question, then click Grade at the bottom.")
st.markdown("---")

# Initialize session state
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'graded' not in st.session_state:
    st.session_state.graded = False

# Display all questions
for idx, row in df.iterrows():
    q_num = row['question_num']
    
    st.markdown(f"**Question {q_num}** ({row['points']} pts)")
    st.markdown(row['question_text'])
    
    answer = st.radio(
        f"Select answer for Q{q_num}:",
        options=['A', 'B', 'C', 'D'],
        format_func=lambda x: f"{x}. {row[f'option_{x.lower()}']}",
        key=f"q{q_num}",
        label_visibility="collapsed"
    )
    
    st.session_state.answers[q_num] = answer
    st.markdown("---")

# Grade button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("📝 Grade My Answers", type="primary"):
        st.session_state.graded = True
with col2:
    if st.button("🔄 Clear All"):
        st.session_state.answers = {}
        st.session_state.graded = False
        st.rerun()

# Show results
if st.session_state.graded:
    st.markdown("---")
    st.header("📊 Results")
    
    total_points = 0
    earned_points = 0
    correct_count = 0
    
    for idx, row in df.iterrows():
        q_num = row['question_num']
        student_answer = st.session_state.answers.get(q_num, '')
        correct_answer = row['correct_answer']
        points = row['points']
        
        total_points += points
        is_correct = (student_answer == correct_answer)
        
        if is_correct:
            earned_points += points
            correct_count += 1
    
    # Display score
    percentage = (earned_points / total_points * 100) if total_points > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Questions Correct", f"{correct_count}/{len(df)}")
    with col2:
        st.metric("Points Earned", f"{earned_points}/{total_points}")
    with col3:
        st.metric("Percentage", f"{percentage:.1f}%")
    with col4:
        if percentage >= 90:
            st.success("A")
        elif percentage >= 80:
            st.info("B")
        elif percentage >= 70:
            st.warning("C")
        else:
            st.error("Review")
    
    st.markdown("---")
    st.subheader("Question-by-Question Results")
    
    for idx, row in df.iterrows():
        q_num = row['question_num']
        student_answer = st.session_state.answers.get(q_num, '')
        correct_answer = row['correct_answer']
        is_correct = (student_answer == correct_answer)
        
        with st.expander(
            f"{'✅' if is_correct else '❌'} Q{q_num}: {row['question_text'][:60]}... "
            f"({'Correct' if is_correct else 'Incorrect'}) - {row['points']} pts"
        ):
            st.markdown(f"**Question:** {row['question_text']}")
            st.markdown(f"**Your answer:** {student_answer}")
            st.markdown(f"**Correct answer:** {correct_answer}")
            if not is_correct:
                st.markdown(f"**Correct option:** {row[f'option_{correct_answer.lower()}']}")
