import streamlit as st
import os
import tempfile
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader, PyPDFLoader

# 1. Page Configuration (Web Interface)
st.set_page_config(page_title="AI SOC Analyst", layout="wide")
st.title("AI SOC INVESTIGATOR (RAG MODEL)")
st.write("Local AI assistant for log analysis and security incidents.")

# Model name (using chr(45) to avoid hyphen parsing issues)
m_id = "all" + chr(45) + "MiniLM" + chr(45) + "L6" + chr(45) + "v2"

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=m_id)

embeddings = get_embeddings()

# 2. Sidebar for Data Upload
with st.sidebar:
    st.header("Data Upload")
    st.write("Supported formats: TXT, PDF, JSON")
    
    uploaded_file = st.file_uploader("Choose a log file", type=["txt", "pdf", "json"])
    process_btn = st.button("Index Logs")

# 3. File Processing Logic
if uploaded_file and process_btn:
    with st.spinner("Loading data into vector database..."):
        temp_ext = "." + uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=temp_ext) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name
        
        try:
            if temp_path.endswith(".pdf"):
                loader = PyPDFLoader(temp_path)
            else:
                loader = TextLoader(temp_path, encoding="utf-8")
                
            docs = loader.load()
            
            vector_db = Chroma.from_documents(
                documents=docs, 
                embedding=embeddings, 
                persist_directory="./db_storage"
            )
            st.success("Knowledge base successfully updated!")
        except Exception as e:
            st.error(f"Processing error: {e}")
        finally:
            os.remove(temp_path)

# 4. Main Chat Window and RAG Logic
st.write("")
query = st.text_input("Enter your query to the analyst (e.g.: Were there any suspicious logins?):")

if query:
    if not os.path.exists("./db_storage"):
        st.warning("Please upload and index logs via the sidebar first!")
    else:
        vector_db = Chroma(persist_directory="./db_storage", embedding_function=embeddings)
        retriever = vector_db.as_retriever()
        
        llm = OllamaLLM(model="llama3")

        template = """You are an experienced SOC Analyst. Analyze the provided logs and answer strictly in the following format:
        
        1. Severity: [Low / Medium / High / Critical]
        2. Event Summary: Brief description of what happened.
        3. Detected IOCs: List of IP addresses, usernames, or suspicious commands.
        4. MITRE ATTACK Mapping: Identify the likely tactic (e.g., Initial Access, Brute Force).
        5. Recommended Actions: Immediate mitigation steps for the system administrator.

        If there is no suspicious activity in the logs, state that clearly.

        LOGS FOR ANALYSIS:
        {context}

        QUESTION: {question}
        
        ANSWER:"""

        prompt = ChatPromptTemplate.from_template(template)
        
        chain = (
            {"context": retriever, "question": RunnablePassthrough()} 
            | prompt 
            | llm 
            | StrOutputParser()
        )

        with st.spinner("Analyzing incident..."):
            try:
                response = chain.invoke(query)
                st.markdown("### INCIDENT REPORT")
                st.info(response)
            except Exception as e:
                st.error(f"Error communicating with the model. Ensure Ollama is running. Details: {e}")
