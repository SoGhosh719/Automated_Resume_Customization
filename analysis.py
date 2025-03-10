import streamlit as st
import PyPDF2
import spacy
import os
from io import BytesIO
from docx import Document
from fpdf import FPDF
from openai import OpenAI

# Ensure spaCy Model is Installed
spacy_model = "en_core_web_sm"
try:
    nlp = spacy.load(spacy_model)
except OSError:
    os.system(f"python -m spacy download {spacy_model}")
    nlp = spacy.load(spacy_model)

# OpenAI API Key (Use Streamlit Secrets Instead of Hardcoding)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip() if text else "No text found in PDF."

# Function to extract key skills from job description
def extract_keywords(job_description):
    doc = nlp(job_description.lower())
    keywords = [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ'] and not token.is_stop]
    return list(set(keywords))  # Remove duplicates

# Function to match resume with job description
def match_skills(resume_text, job_keywords):
    matched_skills = [word for word in job_keywords if word in resume_text.lower()]
    return set(matched_skills)

# Function to generate an improved resume using OpenAI
def improve_resume(resume_text, matched_skills):
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"""
    Here is a resume text:
    {resume_text}

    Please rewrite it to emphasize these skills: {', '.join(matched_skills)}.
    Keep it professional, concise, and in a formal tone. Optimize for ATS compliance.
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message["content"]

# Function to generate a PDF resume
def generate_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add each line separately to prevent overflow
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, txt=line, align="L")

    pdf_output = BytesIO()
    pdf.output(pdf_output, "F")
    pdf_output.seek(0)
    return pdf_output

# Streamlit UI
st.title("📄 Resume Optimizer WebApp")
st.markdown("Upload your **Resume (PDF)** and **Job Description (Text)** to get an optimized resume.")

# File Upload
uploaded_resume = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("📝 Paste Job Description", height=200)

if uploaded_resume and job_description:
    with st.spinner("⏳ Processing..."):
        resume_text = extract_text_from_pdf(uploaded_resume)
        job_keywords = extract_keywords(job_description)
        matched_skills = match_skills(resume_text, job_keywords)

        if matched_skills:
            st.success(f"✅ Matched Skills Found: {', '.join(matched_skills)}")
        else:
            st.warning("⚠️ No significant matches found. Consider adding relevant skills.")

        optimized_resume = improve_resume(resume_text, matched_skills)
        pdf_file = generate_pdf(optimized_resume)

        st.subheader("📥 Download Optimized Resume")
        st.download_button(
            label="📄 Download PDF",
            data=pdf_file,
            file_name="Optimized_Resume.pdf",
            mime="application/pdf"
        )

