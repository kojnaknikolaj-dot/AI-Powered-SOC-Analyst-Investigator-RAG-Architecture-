# Use the official Python image (version 3.11)
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Upgrade pip and install required dependencies
RUN pip install --upgrade pip
RUN pip install streamlit langchain langchain_community langchain_ollama langchain_huggingface chromadb sentence_transformers pypdf

# Expose the port for the Streamlit web interface
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app_soc.py", "--server.port=8501", "--server.address=0.0.0.0"]
