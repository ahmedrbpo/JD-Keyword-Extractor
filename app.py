import streamlit as st
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import spacy
import re
from collections import Counter

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="JD Keyword Extractor with AI Insights",
    page_icon="🔍",
    layout="wide"
)

def initialize_openai_client():
    """Initialize OpenAI client with proper error handling"""
    try:
        # Try multiple ways to get the API key
        api_key = None

        # Method 1: From Streamlit secrets (for deployment)
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            pass

        # Method 2: From environment variables (for local development)
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")

        # Method 3: From user input (fallback)
        if not api_key:
            api_key = st.sidebar.text_input(
                "Enter OpenAI API Key:", 
                type="password",
                placeholder="sk-..."
            )

        if not api_key:
            st.error("❌ OpenAI API Key is required!")
            st.stop()

        # Validate API key format
        if not api_key.startswith(('sk-', 'sk-proj-')):
            st.error("❌ Invalid API Key format! Key should start with 'sk-' or 'sk-proj-'")
            st.stop()

        # Initialize OpenAI client (v1.0+ syntax)
        client = OpenAI(api_key=api_key)
        return client

    except Exception as e:
        st.error(f"❌ Error initializing OpenAI client: {str(e)}")
        st.stop()

def extract_keywords_with_gpt(job_description, client):
    """Extract and categorize keywords using GPT"""
    try:
        prompt = f"""
        Analyze the following job description and extract key technical and soft skills. 
        Categorize them into:
        1. Technical Skills
        2. Soft Skills
        3. Required Qualifications
        4. Preferred Qualifications
        5. Tools & Technologies

        Job Description:
        {job_description}

        Please provide a structured response in the following format:

        **Technical Skills:**
        - skill1
        - skill2

        **Soft Skills:**
        - skill1
        - skill2

        **Required Qualifications:**
        - qualification1
        - qualification2

        **Preferred Qualifications:**
        - qualification1
        - qualification2

        **Tools & Technologies:**
        - tool1
        - tool2
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert HR analyst specializing in job description analysis and keyword extraction."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        st.error(f"❌ Error with OpenAI API: {str(e)}")
        if "401" in str(e):
            st.error("🔑 Authentication failed. Please check your API key.")
        elif "429" in str(e):
            st.error("⏰ Rate limit exceeded. Please wait and try again.")
        elif "quota" in str(e).lower():
            st.error("💳 API quota exceeded. Please check your OpenAI billing.")
        return None

def extract_keywords_nltk(text):
    """Fallback keyword extraction using basic NLP"""
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)

        # Clean and tokenize
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        tokens = word_tokenize(text)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        keywords = [word for word in tokens if word not in stop_words and len(word) > 2]

        # Get most common keywords
        keyword_freq = Counter(keywords)
        return keyword_freq.most_common(20)

    except Exception as e:
        st.warning(f"NLTK extraction failed: {e}")
        return []

def main():
    st.title("🔍 JD Keyword Extractor with AI Insights")
    st.markdown("---")

    # Initialize OpenAI client
    client = initialize_openai_client()

    # Sidebar
    st.sidebar.header("📊 Configuration")
    extraction_method = st.sidebar.selectbox(
        "Choose extraction method:",
        ["AI-Powered (GPT)", "Basic NLP (NLTK)", "Both"]
    )

    # Main interface
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📝 Job Description Input")

        # Input methods
        input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"])

        job_description = ""

        if input_method == "Paste Text":
            job_description = st.text_area(
                "Paste your job description here:",
                height=300,
                placeholder="Copy and paste the job description..."
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload job description file",
                type=['txt', 'docx', 'pdf']
            )
            if uploaded_file is not None:
                # Handle different file types
                if uploaded_file.type == "text/plain":
                    job_description = str(uploaded_file.read(), "utf-8")
                else:
                    st.info("📄 File uploaded. Text extraction from DOCX/PDF requires additional libraries.")

        # Extract button
        if st.button("🚀 Extract Keywords", type="primary"):
            if job_description.strip():
                with st.spinner("🤖 AI is analyzing the job description..."):

                    if extraction_method in ["AI-Powered (GPT)", "Both"]:
                        st.subheader("🤖 AI-Powered Analysis")
                        ai_result = extract_keywords_with_gpt(job_description, client)
                        if ai_result:
                            st.markdown(ai_result)
                        else:
                            st.error("AI analysis failed. Trying fallback method...")
                            extraction_method = "Basic NLP (NLTK)"

                    if extraction_method in ["Basic NLP (NLTK)", "Both"]:
                        st.subheader("📊 Basic NLP Analysis")
                        nltk_keywords = extract_keywords_nltk(job_description)

                        if nltk_keywords:
                            # Display as columns
                            cols = st.columns(3)
                            for i, (keyword, freq) in enumerate(nltk_keywords[:15]):
                                col_idx = i % 3
                                cols[col_idx].metric(
                                    label=keyword.title(),
                                    value=f"{freq} times"
                                )
            else:
                st.warning("⚠️ Please enter a job description first!")

    with col2:
        st.header("ℹ️ Instructions")
        st.markdown("""
        **How to use:**
        1. 🔑 Ensure your OpenAI API key is configured
        2. 📝 Paste or upload your job description
        3. 🎯 Choose extraction method
        4. 🚀 Click "Extract Keywords"

        **API Key Setup:**
        - **Local:** Add to `.env` file
        - **Streamlit Cloud:** Use secrets.toml
        - **Manual:** Enter in sidebar

        **Supported formats:**
        - Plain text (TXT)
        - Microsoft Word (DOCX)*
        - PDF files*

        *Requires additional setup
        """)

        # Troubleshooting section
        with st.expander("🔧 Troubleshooting"):
            st.markdown("""
            **Common Issues:**

            🔑 **Authentication Error (401):**
            - Check API key format
            - Verify key is active
            - Ensure sufficient credits

            ⏰ **Rate Limit (429):**
            - Wait and retry
            - Upgrade API plan

            💾 **Local Setup:**
            ```bash
            pip install openai streamlit python-dotenv nltk
            ```

            🌐 **Streamlit Cloud:**
            - Add secrets in Advanced Settings
            - Format: `OPENAI_API_KEY = "sk-..."`
            """)

if __name__ == "__main__":
    main()
