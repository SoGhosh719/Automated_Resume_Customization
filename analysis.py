import streamlit as st
import spacy
import os
import PyPDF2
from io import BytesIO
from fpdf import FPDF
import openai

# ✅ Load spaCy model from local path (For Offline AI)
spacy_model = "en_core_web_md"  # Use a medium model for better accuracy
try:
    nlp = spacy.load(spacy_model)
except OSError:
    st.error(f"❌ spaCy model `{spacy_model}` not found. Run: `python -m spacy download {spacy_model}`")
    st.stop()

# ✅ Check if OpenAI API key is available
use_api = False
api_key = None
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    openai.api_key = api_key
    use_api = True
except KeyError:
    st.warning("⚠️ No API key found. Using offline AI mode.")

# ✅ Extract text from PDF file
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
        return text.strip() if text.strip() else "⚠️ No readable text found in PDF."
    except Exception as e:
        return f"⚠️ Error reading PDF: {str(e)}"

# ✅ Extract key skills from job description
def extract_keywords(job_description):
    doc = nlp(job_description.lower())
    return list(set(token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ'] and not token.is_stop))

# ✅ Match skills between resume and job description
def match_skills(resume_text, job_keywords):
    return {word for word in job_keywords if word in resume_text.lower()}

# ✅ Improve Resume Using OpenAI API (If Available)
def improve_resume_api(resume_text, matched_skills):
    prompt = f"""
    Rewrite this resume to highlight these skills: {', '.join(matched_skills)}.
    Ensure it is **professional, concise, and ATS-compliant** with quantifiable achievements.

    Original Resume:
    {resume_text}
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error generating resume: {str(e)}"

# ✅ Improve Resume Using Local NLP (No API Mode)
def improve_resume_local(resume_text, matched_skills):
    doc = nlp(resume_text)
    improved_resume = " ".join([token.text if token.text.lower() not in matched_skills else f"**{token.text.upper()}**" for token in doc])
    return improved_resume

# ✅ Generate an optimized resume as a PDF
def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, txt=line.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf_output = BytesIO()
    pdf.output(pdf_output, "F")
    pdf_output.seek(0)
    return pdf_output

# ✅ Streamlit UI
st.title("📄 AI-Powered Resume Optimizer (Hybrid Model)")
st.markdown("🚀 Upload your **resume (PDF)** and paste a **job description** to generate an ATS-friendly optimized resume.")

# ✅ File upload & job description input
uploaded_resume = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("📝 Paste Job Description", height=200)

# ✅ Process & Optimize Resume
if st.button("Optimize Resume"):
    if uploaded_resume and job_description:
        with st.spinner("⏳ Processing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_resume)

            if "⚠️" in resume_text:
                st.error(resume_text)
            else:
                job_keywords = extract_keywords(job_description)
                matched_skills = match_skills(resume_text, job_keywords)

                if matched_skills:
                    st.success(f"✅ Matched Skills: {', '.join(matched_skills)}")
                else:
                    st.warning("⚠️ No matches found. Consider adding relevant skills.")

                # ✅ Use API if available, else use local AI
                if use_api:
                    optimized_resume = improve_resume_api(resume_text, matched_skills)
                else:
                    optimized_resume = improve_resume_local(resume_text, matched_skills)

                if "⚠️" in optimized_resume:
                    st.error(optimized_resume)
                else:
                    pdf_file = generate_pdf(optimized_resume)
                    st.download_button(
                        label="📄 Download Optimized Resume",
                        data=pdf_file,
                        file_name="Optimized_Resume.pdf",
                        mime="application/pdf"
                    )
    else:
        st.warning("⚠️ Please upload a resume and enter a job description.")
