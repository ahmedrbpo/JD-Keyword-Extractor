JD Keyword Extractor - Setup Instructions
🚀 Quick Fix for Common Errors
1. API Key Authentication Issues (401 Error)
The most common issue is improper API key configuration. Here are 3 ways to fix it:
Method A: Using Streamlit Secrets (Recommended for Deployment)
1.	Create folder: .streamlit/
2.	Create file: .streamlit/secrets.toml
3.	Add your key:
OPENAI_API_KEY = "sk-proj-XkpjEgxunLQDWkpuPMuupTVSl7XHxxqZGYG"

Method B: Using Environment Variables (Local Development)
1.	Create .env file in project root
2.	Add: OPENAI_API_KEY=your_key_here
3.	Install: pip install python-dotenv
Method C: Manual Input (Fallback)
The app will prompt for API key in the sidebar if other methods fail.
2. Installation & Setup
# Clone or download the project
git clone https://github.com/ahmedrbpo/JD-Keyword-Extractor
cd JD-Keyword-Extractor

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

3. API Key Validation
✅ Valid formats:
•	sk-proj-... (Project API keys)
•	sk-... (Legacy API keys)
❌ Invalid:
•	Keys without proper prefix
•	Expired or revoked keys
•	Keys with insufficient quota
4. Streamlit Cloud Deployment
1.	Fork/clone repository to GitHub
2.	Connect to Streamlit Cloud
3.	Go to "Advanced settings"
4.	Add secrets in TOML format:
OPENAI_API_KEY = "your_actual_key_here"

🔧 Troubleshooting Common Errors
Error: "The api_key client option must be set"
Fix: Update to OpenAI Python library v1.0+
pip install openai>=1.0.0

Error: "Incorrect API key provided"
Fixes:
1.	Check key format (must start with sk-)
2.	Verify key is active in OpenAI dashboard
3.	Check for extra spaces or characters
4.	Regenerate key if needed
Error: "You exceeded your current quota"
Fixes:
1.	Add payment method to OpenAI account
2.	Check usage limits
3.	Upgrade to paid plan
Error: "Rate limit reached"
Fixes:
1.	Wait and retry
2.	Implement retry logic with backoff
3.	Upgrade API tier
📁 Project Structure
JD-Keyword-Extractor/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (local)
├── .streamlit/
│   └── secrets.toml      # Streamlit secrets (deployment)
└── README.md             # Documentation

🎯 Features Fixed
✅ Proper OpenAI v1.0+ client initialization
✅ Multiple API key source handling
✅ Comprehensive error handling
✅ Fallback keyword extraction (NLTK)
✅ User-friendly error messages
✅ Input validation
✅ Rate limiting awareness
✅ Deployment-ready configuration
