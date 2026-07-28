import streamlit as st

st.set_page_config(page_title="Quiz Generator", page_icon="📝", layout="wide")

# Session State
if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------------- Sidebar ----------------
menu = st.sidebar.radio(
    "Menu",
    ["Add Question", "View Questions", "Start Quiz"]
)

# ---------------- Add Question ----------------
if menu == "Add Question":

    st.title("📝 Add Question")

    with st.form("question_form"):
        question = st.text_input("Question")

        option1 = st.text_input("Option 1")
        option2 = st.text_input("Option 2")
        option3 = st.text_input("Option 3")
        option4 = st.text_input("Option 4")

        correct = st.selectbox(
            "Correct Answer",
            ["Option 1", "Option 2", "Option 3", "Option 4"]
        )

        submit = st.form_submit_button("Add Question")

        if submit:

            if question.strip() == "":
                st.error("Question cannot be empty")

            elif "" in [option1, option2, option3, option4]:
                st.error("All options are required")

            else:
                st.session_state.questions.append({
                    "text": question,
                    "options": [option1, option2, option3, option4],
                    "correct": ["Option 1", "Option 2", "Option 3", "Option 4"].index(correct)
                })

                st.success("Question Added Successfully!")

# ---------------- View Questions ----------------
elif menu == "View Questions":

    st.title("📚 Question Bank")

    if len(st.session_state.questions) == 0:
        st.info("No questions added.")

    else:

        delete_index = None

        for i, q in enumerate(st.session_state.questions):

            with st.expander(f"Q{i+1}. {q['text']}"):

                for j, option in enumerate(q["options"]):

                    if j == q["correct"]:
                        st.success(option)
                    else:
                        st.write(option)

                if st.button("Delete", key=i):
                    delete_index = i

        if delete_index is not None:
            st.session_state.questions.pop(delete_index)
            st.rerun()

# ---------------- Start Quiz ----------------
elif menu == "Start Quiz":

    st.title("🎯 Start Quiz")

    if len(st.session_state.questions) == 0:

        st.warning("Please add questions first.")

    else:

        score = 0

        with st.form("quiz_form"):

            answers = []

            for i, q in enumerate(st.session_state.questions):

                ans = st.radio(
                    q["text"],
                    q["options"],
                    key=f"q{i}"
                )

                answers.append(ans)

            submit = st.form_submit_button("Submit Quiz")

        if submit:

            st.header("📊 Result")

            for i, q in enumerate(st.session_state.questions):

                selected = answers[i]
                selected_index = q["options"].index(selected)

                if selected_index == q["correct"]:
                    score += 1
                    st.success(f"Q{i+1}: Correct")
                else:
                    st.error(f"Q{i+1}: Wrong")
                    st.write("Correct Answer:", q["options"][q["correct"]])

            total = len(st.session_state.questions)
            percentage = (score / total) * 100

            st.divider()

            col1, col2, col3 = st.columns(3)

            col1.metric("Score", f"{score}/{total}")
            col2.metric("Percentage", f"{percentage:.1f}%")

            if percentage >= 90:
                grade = "A+"
            elif percentage >= 75:
                grade = "A"
            elif percentage >= 60:
                grade = "B"
            elif percentage >= 40:
                grade = "C"
            else:
                grade = "Fail"

            col3.metric("Grade", grade)

            st.balloons()