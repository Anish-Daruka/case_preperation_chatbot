import streamlit as st
from case_prep import chain

# Initialize persistent state
if "state" not in st.session_state:
    st.session_state.state = {
        "chat_hist": "No previous conversation",
        "user_query": "",
        "rag_query": "",
        "relevant_docs": [],
        "output": "",
        "intent": ""
    }

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []  # list of (user, assistant)

# Title
st.title("💼 Case Interview Assistant")

if st.session_state.state["chat_hist"] != "No previous conversation":
    with st.expander("🧠 Show Chat Summary (Memory)"):
        st.markdown(st.session_state.state["chat_hist"])

if st.session_state.chat_log:
    # Custom CSS for scrollable chat
    st.markdown(
        """
        <style>
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #f9f9f9;
            margin-top: 1rem;
        }
        .user-msg {
            font-weight: 600;
            margin-top: 1rem;
        }
        .assistant-msg {
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Render chat messages inside styled container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for user_msg, assistant_msg in st.session_state.chat_log:
        st.markdown(f'<div class="user-msg">🧑 You:</div><div class="assistant-msg">{user_msg}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="user-msg">🤖 Assistant:</div><div class="assistant-msg">{assistant_msg}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# Input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        label="",
        placeholder="Type your case prep question here...",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.state["user_query"] = user_input
    with st.spinner("Thinking..."):
        st.session_state.state = chain.invoke(st.session_state.state)
    st.session_state.chat_log.append((user_input, st.session_state.state["output"]))
    st.rerun()



