import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Portuguese": "pt",
    "Russian": "ru",
}

def translate_text(text, source, target):
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_TRANSLATE_API_KEY is not set. Add it to your environment or .env file."
        )

    url = "https://translation.googleapis.com/language/translate/v2"
    data = {"q": text, "target": target, "format": "text"}
    if source != "auto":
        data["source"] = source

    response = requests.post(url, params={"key": api_key}, data=data, timeout=30)
    if not response.ok:
        try:
            message = response.json()["error"]["message"]
        except Exception:
            message = response.text
        raise RuntimeError(f"Translation API error: {message}")

    result = response.json()
    return result["data"]["translations"][0]["translatedText"]

st.set_page_config(page_title="AI Language Translator", page_icon="🌐", layout="centered")
st.title("🌐 AI Language Translation Tool")
st.caption("CodeAlpha Artificial Intelligence Internship — Task 1")

col1, col2 = st.columns(2)
with col1:
    source_name = st.selectbox("Source language", list(LANGUAGES.keys()))
with col2:
    target_options = [x for x in LANGUAGES if x != "Auto Detect"]
    target_name = st.selectbox("Target language", target_options, index=0)

text = st.text_area(
    "Enter text to translate",
    height=180,
    placeholder="Type your sentence or paragraph here..."
)

if st.button("Translate", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Translating..."):
            try:
                result = translate_text(
                    text,
                    LANGUAGES[source_name],
                    LANGUAGES[target_name],
                )
                st.subheader("Translated Text")
                st.text_area("Result", result, height=180)
                st.success("Translation completed successfully.")
            except Exception as exc:
                st.error(str(exc))

st.divider()
st.info("For GitHub submission, keep your API key private and store it in an environment variable.")
