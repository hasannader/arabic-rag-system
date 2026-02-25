# Simple Arabic RAG with Google Gemini

This project demonstrates a **simple RAG (Retrieval-Augmented Generation) system** using Google Gemini APIs. It allows you to query large text documents and get AI-generated answers based on the document’s content.

---

## Features

* Loads a text document and splits it into smaller chunks for better retrieval.
* Converts document chunks into **embeddings** using Google Gemini Embeddings.
* Stores embeddings in a **vector database (FAISS)** for semantic search.
* Uses **Google Gemini Chat** model to answer questions based on retrieved document chunks.
* Returns the answer along with the most relevant chunk and its size.

---

## How It Works

1. **Environment Variables (`.env`)**

   * Store sensitive information like API keys in a `.env` file:

     ```env
     GOOGLE_API_KEY=your_google_api_key_here
     ```
   * The code uses the `dotenv` library to load these variables:

     ```python
     from dotenv import load_dotenv
     import os

     load_dotenv()
     api_key = os.getenv('GOOGLE_API_KEY')
     os.environ["GOOGLE_API_KEY"] = api_key
     ```

2. **Document Loading & Splitting**

   * The `load_document(file_path)` function reads your text file.
   * `RecursiveCharacterTextSplitter` splits the document into chunks (default 500 characters with 100 overlap) for better semantic search.

3. **Embeddings & Vector Store**

   * Each chunk is converted into a **vector embedding** using `GoogleGenerativeAIEmbeddings`.
   * FAISS stores embeddings for **fast similarity search**.

4. **RAG Chain**

   * A **retriever** fetches the most relevant chunks for a question.
   * A **prompt template** guides the LLM to answer questions **based only on the retrieved context**.
   * `ChatGoogleGenerativeAI` generates the final answer.
   * `RunnablePassthrough` and `StrOutputParser` manage the input/output flow of the chain.

5. **Querying**

   ```python
   answer, relevant_chunk, chunk_size = rag.query(user_question)
   ```

   * Returns the AI-generated answer.
   * Shows the **retrieved chunk** and its **size**.

---

## Installation

1. **Clone the repo:**

   ```bash
   git clone https://github.com/yourusername/SimpleRAG.git
   cd SimpleRAG
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

   > The `requirements.txt` file should include packages like:
   >
   > ```
   > python-dotenv
   > langchain
   > faiss-cpu
   > langchain_google_genai
   > ```

4. **Set your `.env` file with your Google API key.**

---

## Usage

```bash
python main.py
```

* Input your question when prompted.
* To exit, type `exit`, `quit`, or `خروج`.

Example output:

```
Total number of chunks in the vector database: 10
اسأل سؤالاً (أو اكتب 'خروج' للإنهاء): ما هو تعريف الذكاء الاصطناعي؟
الجواب: الذكاء الاصطناعي هو ...
المقطع المسترجع: ... (relevant document chunk)
حجم المقطع: 45
```

---

## Notes

* Adjust `chunk_size` and `overlap` in `SimpleRAG` to optimize retrieval.
* This example uses **Gemini Embeddings** and **Gemini Chat**, but it can be adapted for other embedding models.
