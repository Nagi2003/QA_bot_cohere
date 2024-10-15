# Document-Based Question Answering System

## Description

This project implements a question-answering system using Streamlit, Cohere API, and Pinecone for document retrieval and processing.

## Requirements

- Python 3.9
- langchain 
- pinecone-client 
- langchain-cohere 
- langchain-community
- streamlit
- python-dotenv 
- pypdf
- Docker

## Installation

1. Clone the repository:
   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd <YOUR_PROJECT_DIRECTORY>
Build the Docker image by ruuning the command : $ docker build -t qa-bot-cohere .
Run the following command to start the application: $ docker run -p 8501:8501 qa-bot-cohere
Open your browser and navigate to http://localhost:8501 to access the app.
