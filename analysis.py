import streamlit as st
import PyPDF2
import spacy
import os
from io import BytesIO
from docx import Document
from fpdf import FPDF
import openai  # Fix OpenAI client import

# 🔹 Ensure spaCy Model is Installed (Fixed)
spacy_model = "en_core_web_sm"
try:
    nlp = spacy.load(spacy_model)
except OSError:
    st.error(f"❌ `{spacy_model}` model is missing. Ensure it is installed in `requirements.txt`.")
    st.stop()  # Stop execution if model is not installed

# 🔹 OpenAI API Key from Streamlit Secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY  # ✅ Fixed OpenAI Client Initialization

# 🔹 Function to Extract Text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    
    if not text.strip():
        return "⚠️ No readable text found in PDF. Please check the document."
    
    return text.strip()

# 🔹 Function to Extract Key Skills from Job Description
def extract_keywords(job_description):
    doc = nlp(job_description.lower())
    keywords = [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ'] and not token.is_stop]
    return list(set(keywords))  # Remove duplicates

# 🔹 Function to Match Resume with Job Description
def match_skills(resume_text, job_keywords):
    matched_skills = [word for word in job_keywords if word in resume_text.lower()]
    return set(matched_skills)

# 🔹 Function to Generate an Improved Resume using OpenAI
def improve_resume(resume_text, matched_skills):
    prompt = f"""
    Here is a resume text:
    {resume_text}

    Please rewrite it to emphasize these skills: {', '.join(matched_skills)}.
    Ensure it is **professional, concise, and ATS-compliant**.
    """

    response = openai.ChatCompletion.create(  # ✅ Fixed OpenAI API Call
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# 🔹 Function to Generate a PDF Resume
def generate_pdf(text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Wrap text properly to prevent cut-off
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, txt=line, align="L")

    pdf_output = BytesIO()
    pdf.output(pdf_output, "F")
    pdf_output.seek(0)
    return pdf_output

# 🔹 Streamlit UI
st.title("📄 Resume Optimizer WebApp")
st.markdown("Upload your **Resume (PDF)** and **Job Description (Text)** to get an optimized resume.")

# 🔹 File Upload Section
uploaded_resume = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("📝 Paste Job Description", height=200)

if uploaded_resume and job_description:
    with st.spinner("⏳ Processing..."):
        resume_text = extract_text_from_pdf(uploaded_resume)
        
        if "⚠️" in resume_text:
            st.error(resume_text)  # Show error if no text is found in PDF
        else:
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
