import streamlit as st
from main import AITutor

st.set_page_config(page_title="AI Tutor", page_icon="🤖")

st.title("🤖 AI Tutor")
st.write("Ask anything and learn interactively!")

# Initialize tutor
if "tutor" not in st.session_state:
    st.session_state.tutor = AITutor()
    st.session_state.tutor.set_subject("general")

user_input = st.text_input("Ask your question:")

if st.button("Ask"):
    if user_input:
        response = st.session_state.tutor.ask_question(user_input)
        st.write("🤖 Tutor:", response)