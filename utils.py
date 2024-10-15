import os
from io import BytesIO
import cohere
import pinecone
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader  
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere.embeddings import CohereEmbeddings  
from langchain_community.vectorstores import Pinecone as PineconeVectorstore  
from langchain_cohere.llms import Cohere  
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
import tempfile  

def init_services():
    # Load environment variables
    load_dotenv()
    global PINECONE_API_KEY, PINECONE_ENV, COHERE_API_KEY
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    PINECONE_ENV = os.getenv('PINECONE_ENV')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')

    # Initialize Cohere client
    global cohere_client
    cohere_client = cohere.Client(COHERE_API_KEY)

    global pc  
    pc = Pinecone(api_key=PINECONE_API_KEY)  
    
    index_name = "qa-bot-cohere"
    if index_name not in pc.list_indexes().names():
        pc.create_index(name=index_name, dimension=4096, metric='cosine', 
                        spec=ServerlessSpec(cloud='aws', region='us-east-1'))  

def process_uploaded_files(uploaded_files):
    documents = []
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
            
        file_loader = PyPDFLoader(temp_file_path) 
        docs = file_loader.load()
        documents.extend(docs)
        
        os.remove(temp_file_path)

    def chunk_data(docs, chunk_size=800, chunk_overlap=20):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_documents(docs)

    return chunk_data(docs=documents)

def retrieve_answers(query, documents, k=2):
    embeddings = CohereEmbeddings(model="embed-english-v2.0")
    index_name = "qa-bot-cohere"
    pinecone_index = PineconeVectorstore.from_documents(documents, embeddings, index_name=index_name)

    matching_results = pinecone_index.similarity_search(query,k=k)
    
    llm = Cohere(temperature=0.5)
    chain = load_qa_chain(llm, chain_type="stuff")

    response = chain.run(input_documents=matching_results, question=query)
    return response, matching_results
