### **📌 README.md - Automated Resume Customization**
# **🚀 Automated Resume Customization**
A **Streamlit web app** that **optimizes resumes** based on job descriptions using **NLP (`spaCy`) and OpenAI's GPT-4o**. The app extracts key skills, matches them with your resume, and generates an **optimized PDF**.

---

## **📢 Why This Project?**
1. **🚀 Automate resume tailoring** to match job descriptions.  
2. **🤖 Use AI (GPT-4o) to rewrite resumes** to be more ATS-friendly.  
3. **📂 Generate a downloadable PDF** with the improved resume.  
4. **🌍 Deploy on `Railway.app`** to make it publicly accessible.  

---

## **🛠 Features**
✅ **Upload a Resume (PDF)** – Extracts text using `PyPDF2`  
✅ **Paste a Job Description** – Extracts key skills using `spaCy`  
✅ **Match Job Skills with Resume** – Uses NLP to find matching skills  
✅ **Optimize Resume with GPT-4o** – AI improves the resume format  
✅ **Download Improved Resume (PDF)** – Generates a final, ATS-optimized version  
✅ **Fully Deployed on `Railway.app`** – Accessible anywhere  

---

## **🚀 How to Run Locally**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/SoGhosh719/Automated_Resume_Customization.git
cd Automated_Resume_Customization
```

### **2️⃣ Set Up Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the App**
```bash
streamlit run analysis.py
```
🔹 Open **`http://localhost:8501`** in your browser.

---

## **🌍 Deployment on Railway.app**
### **📌 Why Deploy on Railway?**
✅ **Easy GitHub integration**  
✅ **Persistent deployments** (unlike Streamlit Cloud)  
✅ **No missing dependencies**  

### **1️⃣ Create a `Dockerfile`**
Inside the project folder, create a **`Dockerfile`**:
```dockerfile
# ✅ Use Python 3.9 as the base image
FROM python:3.9

# ✅ Set the working directory
WORKDIR /app

# ✅ Install system dependencies (for `spaCy`, `PyPDF2`, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy project files into the container
COPY . .

# ✅ Upgrade pip and install required Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ✅ Download and install spaCy model inside the container
RUN python -m spacy download en_core_web_sm

# ✅ Expose Streamlit's default port
EXPOSE 8501

# ✅ Run Streamlit app
CMD ["streamlit", "run", "analysis.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **2️⃣ Push the Changes to GitHub**
```bash
git add Dockerfile
git commit -m "Added Dockerfile for Railway deployment"
git push origin main
```

### **3️⃣ Deploy on Railway**
1. **Go to [Railway.app](https://railway.app/)**
2. **Click "New Project" → "Deploy from GitHub"**
3. **Select the Repository**
4. **Choose "Docker" as Deployment Method**
5. **Click "Deploy"**  
6. **Copy & Share the App URL! 🎉**

---

## **🛠 Technologies Used**
- **`Streamlit`** → Frontend for UI  
- **`spaCy`** → NLP model for extracting job skills  
- **`OpenAI GPT-4o`** → AI to rewrite resumes  
- **`PyPDF2`** → Extracts text from PDFs  
- **`FPDF`** → Generates optimized resumes as PDFs  
- **`Docker`** → Ensures reliable deployments  
- **`Railway.app`** → Cloud hosting platform  

---

## **👨‍💻 Contributing**
🚀 Want to improve this project? Follow these steps:
1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Automated_Resume_Customization.git
   ```
3. **Create a new branch**:
   ```bash
   git checkout -b feature-branch
   ```
4. **Make changes & commit**:
   ```bash
   git commit -m "Added new feature"
   ```
5. **Push to GitHub & create a Pull Request!**  

---

## **💡 Future Enhancements**
- **🔍 Add Resume Parsing for DOCX** (Word files support)
- **📊 Add Skill Scoring & Matching Percentage**
- **🎨 Improve UI with Streamlit Themes**
- **🤖 AI-based Bullet Point Suggestions**

---

## **📞 Contact**
**👤 Author**: **[SoGhosh719](https://github.com/SoGhosh719)**  
**📧 Email**: `soghosh@clarku.edu`  

---

## **🎯 Final Thoughts**
This project **automates resume customization using AI**, making job applications easier. **Deploying with Docker on Railway ensures a stable, error-free experience.** 🚀  

---
**💡 Ready to use?** 👉 **[Try it on Railway!](https://railway.app/)** 🚀  
