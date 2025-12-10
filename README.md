# MA206 Final Exam Review Materials

## Contents

This package contains materials for reviewing MA206 Probability and Statistics topics:

1. **MA206_Final_Review.tex** - Student review document with practice problems
2. **MA206_Final_Review_Answer_Key.tex** - Complete answer key for instructors
3. **MA206_Review_Answers.csv** - Structured answer data for autograder development
4. **README.md** - This file

## Topics Covered

The review comprehensively covers all topics from the MA206 final exam:

### Section 1: Foundational Concepts
- Observational units and variables
- Categorical vs. quantitative variables
- Study design (observational vs. experimental)
- Appropriate plots for different data types

### Section 2: Parameters, Statistics, and Sampling
- Distinguishing between parameters and statistics
- Sampling methods and bias
- Margin of error calculations
- Generalization and representativeness

### Section 3: Probability Concepts
- Independent events
- Mutually exclusive events
- Conditional probability
- Probability distributions (PMF, PDF, CDF)
- Bayes' Theorem

### Section 4: Hypothesis Testing
- Selecting appropriate statistical tests
- One-proportion z-test
- One-sample t-test
- Two-proportion z-test
- Two-sample t-test
- Paired t-test
- Correlation and regression

### Section 5-7: Inference Procedures
- One-proportion z-test (detailed)
- Two-sample t-test (detailed)
- Paired t-test (detailed)

### Section 8-9: Regression Analysis
- Simple linear regression
- Multiple linear regression
- Interpretation of coefficients
- Interaction terms
- Model selection

### Section 10: Confounding Variables
- Identifying confounding variables
- Random assignment
- Causal inference

### Section 11-13: Probability Theory
- Bayes' Theorem applications
- Expected value and variance
- Discrete random variables
- Linear transformations of random variables

### Section 14: Continuous Random Variables
- PDFs and CDFs
- Calculating probabilities from continuous distributions

### Section 15: Mixed Practice
- Confidence interval interpretation
- Type I and Type II errors
- Regression diagnostics

## Using the Review Materials

### For Students

1. **Compile the LaTeX file**: Use any LaTeX compiler to create a PDF
   ```bash
   pdflatex MA206_Final_Review.tex
   ```

2. **Work through problems**: Answer each question completely, showing all work

3. **Use R/RStudio**: Many problems require statistical software
   - Load datasets as instructed
   - Perform hypothesis tests
   - Create visualizations
   - Calculate confidence intervals

4. **Round to 3 significant digits**: Unless otherwise specified

### For Instructors

1. **Answer Key**: The complete answer key is in `MA206_Final_Review_Answer_Key.tex`

2. **Customization**: Both LaTeX files can be easily modified:
   - Change problem numbers
   - Adjust difficulty
   - Add/remove sections
   - Modify contexts to match your course

## Building the Streamlit Autograder

The `MA206_Review_Answers.csv` file is structured for easy autograder development.

### CSV Structure

```
problem_id,question_part,answer_type,correct_answer,alternative_answers,points
```

- **problem_id**: Unique identifier (e.g., "1.1a", "5c")
- **question_part**: Brief description of the question
- **answer_type**: "numeric", "text", or "multiple_choice"
- **correct_answer**: Primary correct answer
- **alternative_answers**: Pipe-separated acceptable variations (e.g., "0.58|58%|0.580")
- **points**: Point value for the question

### Streamlit App Structure (Recommended)

```python
import streamlit as st
import pandas as pd
import numpy as np

# Load answer key
answers = pd.read_csv('MA206_Review_Answers.csv')

# Create sections
sections = {
    'Section 1': ['1.1a', '1.1b', '1.1c', ...],
    'Section 2': ['2.1a', '2.1b', ...],
    # etc.
}

# Main app
st.title("MA206 Final Review Autograder")

# Select section
section = st.sidebar.selectbox("Choose a section", list(sections.keys()))

# Display questions and collect answers
student_answers = {}

for problem_id in sections[section]:
    question_data = answers[answers['problem_id'] == problem_id].iloc[0]
    
    st.subheader(f"Problem {problem_id}")
    st.write(question_data['question_part'])
    
    if question_data['answer_type'] == 'numeric':
        student_answers[problem_id] = st.number_input(
            f"Your answer for {problem_id}",
            key=problem_id
        )
    elif question_data['answer_type'] == 'text':
        student_answers[problem_id] = st.text_input(
            f"Your answer for {problem_id}",
            key=problem_id
        )

# Grading function
def grade_answer(problem_id, student_answer):
    """Grade a single answer"""
    correct = answers[answers['problem_id'] == problem_id].iloc[0]
    
    if correct['answer_type'] == 'numeric':
        # Allow small tolerance for rounding
        try:
            return abs(float(student_answer) - float(correct['correct_answer'])) < 0.01
        except:
            return False
    
    elif correct['answer_type'] == 'text':
        # Check against correct answer and alternatives
        student_lower = str(student_answer).lower().strip()
        correct_lower = correct['correct_answer'].lower().strip()
        
        if student_lower == correct_lower:
            return True
        
        # Check alternatives
        if pd.notna(correct['alternative_answers']):
            alternatives = correct['alternative_answers'].lower().split('|')
            return any(alt.strip() == student_lower for alt in alternatives)
    
    return False

# Submit button
if st.button("Grade My Answers"):
    total_points = 0
    earned_points = 0
    
    for problem_id, student_answer in student_answers.items():
        question_data = answers[answers['problem_id'] == problem_id].iloc[0]
        total_points += question_data['points']
        
        if grade_answer(problem_id, student_answer):
            earned_points += question_data['points']
            st.success(f"✓ Problem {problem_id}: Correct!")
        else:
            st.error(f"✗ Problem {problem_id}: Incorrect")
            if st.checkbox(f"Show answer for {problem_id}"):
                st.info(f"Correct answer: {question_data['correct_answer']}")
    
    st.write("---")
    st.write(f"### Score: {earned_points}/{total_points} ({100*earned_points/total_points:.1f}%)")
```

### Advanced Features to Consider

1. **Show Work Section**: Allow students to upload images or type explanations
2. **Partial Credit**: Implement rubric-based grading for multi-step problems
3. **Hints System**: Provide progressive hints
4. **Progress Tracking**: Save student progress across sessions
5. **Detailed Feedback**: Explain why answers are incorrect
6. **Formula Reference**: Include a formula sheet
7. **Practice Mode**: Show answers immediately vs. exam mode
8. **Analytics Dashboard**: Track performance by topic area

### Deployment

```bash
# Install Streamlit
pip install streamlit pandas numpy

# Run locally
streamlit run autograder_app.py

# Deploy to Streamlit Cloud
# 1. Push code to GitHub
# 2. Connect to streamlit.io
# 3. Deploy
```

## Additional Notes

### Tolerance for Numerical Answers

- Use appropriate tolerance (e.g., ±0.01 for 3 significant digits)
- Consider rounding errors
- Accept scientific notation variations

### Text Answer Matching

- Case-insensitive matching
- Strip whitespace
- Accept common synonyms (included in alternative_answers)
- Consider fuzzy matching for minor typos

### R Code Integration

Consider adding:
- Code snippets for each problem type
- Expected R output format
- Common errors to avoid

## Customization Tips

### Modifying Questions

To add new problems:
1. Add to LaTeX files
2. Add corresponding entry to CSV
3. Update Streamlit app section mapping

### Adjusting Difficulty

- Change numerical values
- Modify contexts
- Add/remove steps
- Include/exclude hints

### Course-Specific Adaptation

- Update datasets to match your course
- Modify terminology
- Adjust significance levels
- Change R packages if needed

## Technical Requirements

### For LaTeX Compilation
- LaTeX distribution (TeX Live, MiKTeX, etc.)
- Required packages: amsmath, amssymb, enumitem, hyperref

### For Streamlit App
- Python 3.7+
- streamlit
- pandas
- numpy

## License and Attribution

These materials are designed for MA206 at the United States Military Academy.
Feel free to adapt for your own course with appropriate attribution.

## Support

For questions or issues:
- Check the answer key for solution methods
- Review the CSV file for answer formats
- Test the Streamlit app with sample data

## Version History

- v1.0 (December 2025): Initial release covering all final exam topics

---

**Good luck with your studying!**
