# ✅ Use Python 3.9 as the base image
FROM python:3.9

# ✅ Set the working directory
WORKDIR /app

# ✅ Copy project files into the container
COPY . .

# ✅ Upgrade pip and install required Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ✅ Expose Streamlit's default port
EXPOSE 8501

# ✅ Run Streamlit app
CMD ["streamlit", "run", "analysis.py", "--server.port=8501", "--server.address=0.0.0.0"]
