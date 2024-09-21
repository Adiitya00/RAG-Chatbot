# RAG-Chatbot
A RAG Chatbot using hybrid retrieval search with Langchain and pinecone vector database 
# Project Overview
The project aims to create a hybrid search chatbot using a combination of Langchain, Pinecone, and a PDF document as a knowledge base. The chatbot enables users to ask questions based on the contents of the PDF and retrieves relevant information using hybrid search techniques.

# Decisions Made
### Use of Pinecone: 
Pinecone was chosen as the vector database for its efficiency in managing large-scale embeddings and enabling fast retrieval of relevant information.
### Langchain for Retrieval: 
Langchain provides a robust framework for building conversational agents, making it easier to integrate retrieval and generation capabilities.
### PDF Processing: 
PyPDF2 was utilized for extracting text from PDF files, enabling the chatbot to answer questions based on document contents.
Challenges Faced
### Extracting Text from PDFs: 
Different PDFs may have varying structures, leading to challenges in reliably extracting text. Some PDFs may not be formatted in a way that allows for clean text extraction.
### Handling Large Documents: 
With larger PDFs, storing and retrieving text efficiently while ensuring relevant context is retained posed a challenge.
### Integrating Components: 
Ensuring seamless communication between the various components (PDF extraction, Pinecone indexing, and Langchain querying) required careful planning and testing.
# Solutions
### Text Extraction Handling: 
Implemented fallback mechanisms to ensure that if a PDF is not parsed correctly, the user is informed and prompted to upload a different file.
### Chunking Text: 
For large documents, the text was chunked into manageable sizes to ensure effective indexing and retrieval without losing context.
Modular Design: Structured the code into separate functions for text extraction, query handling, and user interface to improve maintainability and clarity.

# Model Architecture

### Document Processing: 
This module is responsible for reading and extracting text from uploaded PDF files. It breaks the content into manageable chunks for effective indexing and retrieval.

### Retrieval Mechanism: 
Utilizing Pinecone, a vector database, the retrieval mechanism employs both dense and sparse search techniques:

Dense Retrieval: This uses embeddings generated from the text to retrieve semantically similar content.
Sparse Retrieval: This leverages the BM25 algorithm to rank documents based on term frequency and other statistical measures.

### Response Generation:
Once the relevant documents are retrieved, the chatbot formulates responses by combining the retrieved information. This is done using template-based generation to ensure clarity and conciseness in the answers.

# Approach to Retrieval
### Text Extraction: 
The application uses the PyPDF2 library to extract text from PDF documents. This process includes:
Reading each page of the PDF.
Extracting the text and storing it in a structured format (e.g., chunks or sentences).
Indexing
### Pinecone Integration: 
The extracted text chunks are indexed using Pinecone, allowing for efficient querying. 
The indexing process includes:
Generating embeddings for the text chunks using a pre-trained model (e.g., all-MiniLM-L6-v2).
Storing these embeddings in Pinecone for quick retrieval during user queries.
Query Processing
When a user submits a query, the application performs the following steps:
Embedding the Query: The user's input is converted into an embedding using the same model used for indexing.
### Hybrid Search:
Sparse Search: The BM25 algorithm ranks the indexed documents based on the keyword matches.
Dense Search: The embedding of the query is compared to the embeddings of the indexed documents to find semantically relevant matches.
Result Compilation: 
The results from both the dense and sparse searches are combined, weightage, and filtered to produce a final list of relevant documents.

# Generative Response Creation
Contextual Information: The chatbot selects key information from the retrieved documents based on the user's query.

Template-Based Generation: Using pre-defined templates, the chatbot formulates responses that provide clear and concise answers. This helps in maintaining the context while ensuring that the user receives an informative reply.

User Interaction: The final response is then displayed to the user in the chat interface, providing a seamless interaction experience.

# Pipeline Documentation
PDF Upload: Users upload a PDF document through the interface.
Text Extraction: The uploaded PDF is processed to extract text.
Indexing with Pinecone: Extracted text chunks are indexed using Pinecone for fast retrieval.
User Query: Users can input queries, which are processed to find relevant answers from the indexed text.
Response Display: The chatbot displays the retrieved answer in the interface.

# Requirements for installtion
pinecone-client
langchain
openai
PyPDF2
streamlit
sentence-transformers
pinecone-text
pinecone-notebooks
python-dotenv
langchain-community
langchain-huggingface

"pip install -r requirements.txt" Run this command to install all this libries

# Dockerfile Creation
Create a Dockerfile in the root of your project directory. This file will define the environment for your application.

Use the official Python image from the Docker Hub
FROM python:3.9-slim

Set the working directory
WORKDIR /app

Copy requirements.txt to the container
COPY requirements.txt .

Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

Copy the application code to the container
COPY . .

Expose the port that Streamlit runs on
EXPOSE 8501

Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
Step 2: Build the Docker Image
In your terminal, navigate to your project directory and run the following command to build the Docker image:
"docker build -t advanced-hybrid-search-chatbot"

Step 3: Run the Docker Container
After building the image, you can run the Docker container using:
"docker run -p 8501:8501 advanced-hybrid-search-chatbot"

