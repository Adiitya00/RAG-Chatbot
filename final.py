# Import required libraries
import os
import pinecone as pc
from pinecone import ServerlessSpec
from dotenv import load_dotenv
from langchain_community.retrievers import PineconeHybridSearchRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder
import PyPDF2
import streamlit as st

# Set a api key
api_key = ""  # replace with your pinecone api key

# Set up Pinecone database 
index_name = "adi"
pc = pc.Pinecone(api_key=api_key) 
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="dotproduct",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Load environment variables
load_dotenv()
os.environ['Hf_Token'] = ''  # replace with your huggingface Token

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize BM25 Encoder
bm25_encoder = BM25Encoder().default()

# Streamlit UI for file upload
st.set_page_config(page_title="Hybrid Search RAG Chatbot", page_icon="🤖", layout="wide")
st.title("Hybrid Search RAG Chatbot")
st.markdown("<h2 style='text-align: center;'>Upload a PDF and Ask Questions!</h2>", unsafe_allow_html=True)

# Sidebar for file upload
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Read and process the PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text_chunks = []
    for page in pdf_reader.pages:
        text = page.extract_text()
        text_chunks.append(text)

    # Fit BM25 encoder on the text chunks
    bm25_encoder.fit(text_chunks)
    bm25_encoder.dump("bm25_values.json")
    bm25_encoder = BM25Encoder().load("bm25_values.json")

    # Initialize the retriever
    retriever = PineconeHybridSearchRetriever(index_name=index_name, embeddings=embeddings, sparse_encoder=bm25_encoder)
    retriever.add_text(text_chunks)

    # Input for querying
    st.markdown("<h3 style='text-align: center;'>Ask Your Question</h3>", unsafe_allow_html=True)
    query = st.text_input("Enter your query:", key="query_input")

    if st.button("Ask", key="ask_button"):
        if query:
            results = retriever.invoke(query)
            st.markdown(f"<div style='text-align: left; background-color: #f9f9f9; padding: 10px; border-radius: 5px;'>**Results:** {results}</div>", unsafe_allow_html=True)

# Footer section
st.markdown(
    """
    <hr style="border:0.5px solid gray;">
    <div style="text-align: center;">
        <p style="font-size: 16px;">Developed by Aditya Kamble | 2024</p>
    </div>
    """, unsafe_allow_html=True
)
