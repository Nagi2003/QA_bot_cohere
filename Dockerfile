
FROM python:3.9

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port for Streamlit 
EXPOSE 8501

# Set working directory
WORKDIR /app

# Command to run the application
CMD ["streamlit", "run", "app.py"] 

## docker build -t document-qa .
## docker run -p 8501:8501 document-qa