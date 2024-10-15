import streamlit as st
from utils import process_uploaded_files, retrieve_answers, init_services

init_services()


st.markdown("<h1 style='text-align: center; color: grey;'>Document-Based Question Answering System</h1>", unsafe_allow_html=True)


uploaded_files = st.file_uploader("Upload your PDF documents", type="pdf", accept_multiple_files=True)

if uploaded_files:
    documents = process_uploaded_files(uploaded_files)

    user_query = st.text_input("Ask a question based on the uploaded documents:")

    if user_query:
        answer, retrieved_docs = retrieve_answers(user_query, documents)

        # Display answer
        st.write("Answer:")
        st.write(answer)
