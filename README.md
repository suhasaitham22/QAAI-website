# QAAI Website (Interview Preparation Tool)

An interview preparation tool for job seekers, especially students and recent graduates. Upload your resume (PDF or DOCX), paste a job description, and the app uses OpenAI's GPT to generate tailored interview questions plus suggested answers grounded in your resume.

## How it works

`code.py` is a three-page Streamlit app with sidebar navigation:

1. **Introduction** — what the tool does and the tech behind it.
2. **Upload Resume** — upload a PDF or DOCX resume (parsed with PyMuPDF or python-docx), paste the job description or title, choose how many questions you want (10, 25, or 50), and hit "Generate Interview Questions". The app calls `gpt-3.5-turbo` (max 500 tokens) with a prompt built from your resume text and the job description, then lists the questions.
3. **Generate Answers** — for each generated question, the app calls `gpt-3.5-turbo` again (max 200 tokens) to draft a suggested answer based on your resume.

Questions and the parsed resume text are kept in Streamlit session state so the pages share them.

A live demo is available at https://appai-website-baznfwzocvbxrqubqnwicf.streamlit.app/

## Install and run

```bash
git clone https://github.com/suhasaitham22/QAAI-website.git
cd QAAI-website
pip install -r requirements.txt
```

Add your OpenAI API key to `.streamlit/secrets.toml` (the app reads `st.secrets["api"]["OPEN_API_KEY"]`):

```toml
[api]
OPEN_API_KEY = "sk-your-key-here"
```

Then:

```bash
streamlit run code.py
```

## Tech stack

Streamlit, OpenAI API (gpt-3.5-turbo), PyMuPDF, python-docx.
