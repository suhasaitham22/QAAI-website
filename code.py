import streamlit as st
import openai
import fitz  # PyMuPDF
import docx

# Set up OpenAI API key
openai.api_key = st.secrets["api"]["OPEN_API_KEY"]

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
    
    try:
        with st.spinner('Generating questions...'):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            questions = response.choices[0].message['content'].strip().split('\n')
            return questions
    except Exception as e:
        st.error(f"Error generating questions: {e}")
        return []

# Function to generate answers using OpenAI
def generate_answer(resume_text, question):
    prompt = f"Based on the following resume: '{resume_text}', provide an answer to this interview question: '{question}'"
    
    try:
        with st.spinner('Generating answer...'):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"Error generating answer: {e}")
        return "Error generating answer."

# Page 1: Introduction
# Page 1: Introduction
def show_introduction():
    st.header("Introduction")
    
    st.write("""
    This application is designed to assist job seekers, particularly students and recent graduates, in preparing for job interviews by generating tailored interview questions and suggested answers based on their resumes and the job descriptions they are targeting.
    
    ### Main Idea
    The main idea behind this tool is to streamline the interview preparation process. By leveraging AI technologies, it analyzes the content of resumes and correlates it with job descriptions to provide relevant questions that candidates may face during interviews. This not only helps users anticipate potential questions but also enables them to formulate structured and informed responses that highlight their qualifications and experiences.

    ### Technologies Used
    - **Streamlit**: A powerful framework for building interactive web applications quickly, allowing users to interact with the tool easily.
    - **OpenAI's GPT Model**: Utilized to generate insightful interview questions and answers based on the user's resume and desired job description. This AI model is trained on a diverse range of topics, making it capable of providing meaningful and contextually relevant content.
    - **PyMuPDF and python-docx**: Libraries used for parsing PDF and DOCX resume files, allowing users to upload their resumes seamlessly.
    
    ### Benefits for Students and Job Seekers
    - **Tailored Preparation**: Users receive personalized interview questions that are specific to their resumes and job aspirations, enhancing their preparation strategy.
    - **Confidence Building**: By practicing with AI-generated questions and suggested answers, candidates can build their confidence before actual interviews, leading to improved performance.
    - **Accessibility**: The tool is easy to use and can be accessed from anywhere, making it a convenient resource for anyone looking to improve their interview skills.
    - **Time Efficiency**: Instead of spending hours searching for common interview questions or writing down responses, users can quickly generate and refine their answers, allowing them to focus on other aspects of their job search.

    This tool is not only beneficial for students but also for anyone looking to enhance their interview skills and secure their desired job.
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
