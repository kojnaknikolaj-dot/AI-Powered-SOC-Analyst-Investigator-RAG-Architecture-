AI-Powered SOC Analyst Investigator (RAG Architecture)

    About the Project

This project is a locally hosted, AI-driven tool designed to automate the workflow of a Cybersecurity Analyst (SOC L1/L2).
It tackles the critical issue of "Alert Fatigue" by allowing analysts to investigate massive volumes of unstructured logs (TXT, JSON) and Threat Intelligence reports (PDF) using natural language queries.

The core advantage of this project is 100% Data Privacy. By leveraging a localized Llama 3 model (via Ollama), it ensures that sensitive corporate logs never leave the secure network perimeter, strictly avoiding third-party cloud APIs (like OpenAI).

    Technology Stack

Language: Python

LLM & AI: Llama 3 (via Ollama), LangChain, HuggingFace (all-MiniLM-L6-v2)

Vector Database: ChromaDB

Frontend UI: Streamlit

Infrastructure: Docker, Docker Compose

   Key Features

Automated Ingestion: Upload and chunk unstructured data (Syslog, Auth.log, Windows Events) and reports (PDF) directly via the web interface.

Semantic Vectorization: Converts logs into embeddings for rapid semantic search and context retrieval.

Automated Incident Reporting: The LLM generates structured reports strictly adhering to SOC standards:

Severity Level Assessment

Event Summary

Detected IOCs (Indicators of Compromise: IPs, Users)

MITRE ATT&CK Framework Mapping

Recommended Mitigation Actions

    Installation & Usage

Option 1: Run via Docker (Recommended)

Ensure you have Docker and Ollama installed on your host machine.
First, pull the Llama 3 model in your terminal:

ollama pull llama3


Then, run the following command in the project directory:

docker-compose up --build


(Note: If your system uses an underscore, run docker_compose up --build)
The application will be accessible at: http://localhost:8501

Option 2: Local Python Execution

Activate your virtual environment.

Install the required dependencies:

pip install streamlit langchain langchain_community langchain_ollama langchain_huggingface chromadb sentence_transformers pypdf


Launch the Streamlit web interface:

streamlit run app_soc.py


     Use Case Example

Upload an auth.log containing brute-force attempts.

Ask: "Were there any suspicious login attempts? Identify the source IP."

Receive a full, actionable Incident Report mapped to MITRE ATT&CK.
