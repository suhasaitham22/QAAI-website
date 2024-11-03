import streamlit as st
import openai
import fitz  # PyMuPDF
import docx
from transformers import pipeline
from setuptools import find_packages

# open_api_key = st.secrets["api"]["OPEN_API_KEY"]

# Function to parse resume content from PDF or DOCX
def parse_resume(file):
    if file.type == "application/pdf":
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = "\n".join(page.get_text() for page in doc)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
        text = ""
    return text

# Function to generate interview questions using OpenAI
def generate_questions(resume_text, job_description, num_questions=10):
    prompt = f"Generate {num_questions} interview questions based on the resume: '{resume_text}' and job description: '{job_description}'."
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=500)
    return response.choices[0].text.strip().split('\n')

# Function to generate answers using OpenAI
def generate_answer(resume_text, question):
    prompt = f"Based on the following resume: '{resume_text}', provide an answer to this interview question: '{question}'"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=200)
    return response.choices[0].text.strip()

# Page 1: Introduction
def show_introduction():
    st.header("Introduction")
    st.write("""
    This tool helps job seekers prepare for interviews by analyzing their resumes and generating 
    potential interview questions and answer suggestions based on the job they’re targeting.
    """)

# Page 2: Resume Upload and Question Generation
def show_upload_page():
    st.header("Upload Resume and Enter Job Description")
    resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Enter the job description or title")

    if resume_file and job_description:
        resume_text = parse_resume(resume_file)
        num_questions = st.selectbox("Select number of questions", options=[10, 25, 50])
        
        if st.button("Generate Interview Questions"):
            questions = generate_questions(resume_text, job_description, num_questions)
            st.session_state['questions'] = questions
            st.session_state['resume_text'] = resume_text
            st.write("### Interview Questions")
            for i, question in enumerate(questions, 1):
                st.write(f"{i}. {question}")

# Page 3: Answer Generation
def show_answers_page():
    if 'questions' in st.session_state and 'resume_text' in st.session_state:
        st.header("Suggested Answers")
        questions = st.session_state['questions']
        resume_text = st.session_state['resume_text']
        
        for i, question in enumerate(questions, 1):
            answer = generate_answer(resume_text, question)
            st.write(f"### Question {i}: {question}")
            st.write(f"**Suggested Answer:** {answer}")
    else:
        st.write("Please generate questions first by going to the 'Upload Resume' page.")

# Navigation in Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ["Introduction", "Upload Resume", "Generate Answers"])

if page == "Introduction":
    show_introduction()
elif page == "Upload Resume":
    show_upload_page()
elif page == "Generate Answers":
    show_answers_page()
