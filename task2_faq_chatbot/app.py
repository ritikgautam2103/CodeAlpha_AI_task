import streamlit as st
from chatbot import FAQChatbot

st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖")
st.title("🤖 FAQ Chatbot")
st.caption("CodeAlpha Artificial Intelligence Internship — Task 2")

@st.cache_resource
def load_bot():
    return FAQChatbot()

bot = load_bot()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message.get("meta"):
            st.caption(message["meta"])

question = st.chat_input("Ask a frequently asked question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    answer, score, matched = bot.answer(question)
    meta = f"Similarity: {score:.2f}"
    if matched:
        meta += f" | Matched FAQ: {matched}"

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "meta": meta}
    )
    with st.chat_message("assistant"):
        st.write(answer)
        st.caption(meta)

st.divider()
st.write("**Method:** NLP preprocessing → TF-IDF → cosine similarity → best FAQ response.")
