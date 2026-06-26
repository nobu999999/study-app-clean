import streamlit as st
from database import get_random_problem
import streamlit.components.v1 as components

def speak_button(text):
    components.html(f"""
        <button onclick="
            const msg = new SpeechSynthesisUtterance(`{text}`);
            msg.lang = 'en-US';
            msg.rate = 0.9;
            window.speechSynthesis.speak(msg);
        ">
            🔊 英語を聞く
        </button>
    """, height=50)

st.title("英語復唱モード")

if "english_problem" not in st.session_state:
    st.session_state.english_problem = get_random_problem("english")
    st.session_state.show_answer = False

problem = st.session_state.english_problem

if problem is None:
    st.warning("英語問題がまだ登録されていません")
else:
    problem_id, question, answer, memo = problem

    st.subheader("日本語")
    st.write(question)

    if st.button("答えを見る"):
        st.session_state.show_answer = True

    if st.session_state.show_answer:
        st.subheader("英語")
        st.write(answer)
        speak_button(answer)

        if memo:
            st.caption(memo)

        if st.button("次の問題"):
            st.session_state.english_problem = get_random_problem("english")
            st.session_state.show_answer = False
            st.rerun()

