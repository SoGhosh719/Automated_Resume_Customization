# ✅ Use Python 3.9 as the base image
FROM python:3.9

# ✅ Set the working directory
WORKDIR /app

# ✅ Install system dependencies (ensures compatibility with spaCy & PDF handling)
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

# ✅ Run Streamlit app (Final fix: Use `exec` format to prevent crashes)
CMD exec streamlit run analysis.py --server.port=8501 --server.address=0.0.0.0
