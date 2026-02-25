import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

# Fetch the API key
api_key = os.getenv('GOOGLE_API_KEY')

# Configure the Gemini API key
os.environ["GOOGLE_API_KEY"] = api_key # Set the API key
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

def load_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

class SimpleRAG:
    def __init__(self, file_path, chunk_size=500, overlap=100):
        # Load the document
        text = load_document(file_path)

        # Split the text into documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap) ####### RecursiveCharacterTextSplitter
        self.docs = text_splitter.create_documents([text]) # Store docs as an instance variable

        # Create embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", google_api_key=api_key)

        # Create a vector store and retriever
        vector_store = FAISS.from_documents(self.docs, embeddings) # Use self.docs here
        self.retriever = vector_store.as_retriever() ########## top 4 by default

        # Initialize the LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.3)

        # Define the prompt template
        template = """Answer the following question based only on the provided context:

        Context:
        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        # Create the RAG chain using LCEL
        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def get_total_chunks(self):
        return len(self.docs)

    def query(self, question):
        # Get the answer from the chain
        answer = self.chain.invoke(question)

        # For demonstration, we'll retrieve the relevant docs again to show the source
        relevant_docs = self.retriever.invoke(question)  # Use invoke to handle run_manager internally ## Semantic Similarity
        if relevant_docs:
            relevant_chunk = relevant_docs[0].page_content
            chunk_size = len(relevant_chunk.split()) # Changed to word count
        else:
            relevant_chunk = "No relevant chunk found."
            chunk_size = 0

        return answer, relevant_chunk, chunk_size

if __name__ == '__main__':
    rag = SimpleRAG('arabic.txt')
    total_chunks = rag.get_total_chunks()
    print(f"Total number of chunks in the vector database: {total_chunks}")
    while True:
        user_question = input("اسأل سؤالاً (أو اكتب 'خروج' للإنهاء): ")
        if user_question.lower() in ['exit', 'quit', 'خروج']:
            break
        answer, chunk, chunk_size = rag.query(user_question)

        print("\nالجواب:", answer)
        print("المقطع المسترجع:", chunk)
        print("حجم المقطع:", chunk_size)
        print("-" * 20, "\n")