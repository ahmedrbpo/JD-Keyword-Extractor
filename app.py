import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="JD Keyword Extractor", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .main {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
        }
        h1, h2, h3 {
            color: #003366;
        }
        .stTextInput > div > input {
            color: #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🧠 Job Description Keyword Extractor</h1>", unsafe_allow_html=True)
st.markdown("---")

with st.container():
    st.markdown("### 📝 Paste Job Description")
    jd_text = st.text_area("Enter the job description below", height=300)

if st.button("🔍 Extract Keywords"):
    if not jd_text.strip():
        st.warning("⚠️ Please enter a job description before clicking extract.")
    else:
        with st.spinner("Extracting keywords using GPT..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that extracts and categorizes keywords."},
                        {"role": "user", "content": f"Extract and categorize keywords from this job description:\n{jd_text}"}
                    ]
                )
                result = response.choices[0].message.content
                st.success("✅ Extraction complete!")
                st.markdown("### 🔑 Extracted Keywords & Categories")
                st.markdown(f"<div style='background-color:#eef;border-left:5px solid #003366;padding:10px;'>{result}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {e}")
