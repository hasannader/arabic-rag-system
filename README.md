# Simple Arabic RAG with Google Gemini

This project implements a **Retrieval-Augmented Generation (RAG)** system for answering questions based on an Arabic text file using **Google Gemini** and **LangChain**.

The application:

* Loads an Arabic document
* Splits it into chunks
* Converts chunks into embeddings
* Stores them in a FAISS vector database
* Retrieves the most relevant chunks
* Generates answers using Gemini based only on the retrieved context

---

## Project Structure

```
.
├── rag_app.py          # Main application
├── arabic.txt          # Knowledge base (Arabic text)
├── requirements.txt    # Python dependencies
├── .env                # Contains API key (not uploaded)
└── README.md
```

---

## How It Works

### 1. Load Environment Variables

The app reads your Google API key from a `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

This key is required to access:

* Gemini Chat Model
* Gemini Embeddings

The key is loaded using:

```python
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
```

---

### 2. Document Processing

* The file `arabic.txt` is loaded.
* The text is split using:

  ```
  RecursiveCharacterTextSplitter
  ```
* Default settings:

  * Chunk size: 500 characters
  * Overlap: 100 characters

This improves semantic retrieval and keeps context continuity.

---

### 3. Embeddings & Vector Database

* Each chunk is converted into a vector using:

  ```
  GoogleGenerativeAIEmbeddings
  ```
* Vectors are stored in:

  ```
  FAISS (local vector database)
  ```
* During a query, the system retrieves the **top relevant chunks** using semantic similarity.

---

### 4. RAG Pipeline

The pipeline:

1. User asks a question
2. Relevant chunks are retrieved
3. Context + question are inserted into a prompt
4. Gemini generates the answer
5. The system also shows:

   * Retrieved chunk
   * Chunk word count

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/arabic-rag.git
cd arabic-rag
```

---

### 2. Create a virtual environment (recommended)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add your API key

Create a file named `.env`:

```
GOOGLE_API_KEY=your_google_api_key_here
```

⚠️ Do **not** upload your `.env` file to GitHub.
Add it to `.gitignore`.

---

## Usage

Run the application:

```bash
python rag_app.py
```

Example:

```
Total number of chunks in the vector database: 12
اسأل سؤالاً (أو اكتب 'خروج' للإنهاء): ما هو الذكاء الاصطناعي؟

الجواب: ...
المقطع المسترجع: ...
حجم المقطع: 45
```

Type:

* `exit`
* `quit`
* `خروج`

to stop the program.

---

## Customization

You can modify chunk settings inside `SimpleRAG`:

```python
SimpleRAG(file_path, chunk_size=500, overlap=100)
```

Larger chunks = more context
Smaller chunks = faster retrieval

---

## Technologies Used

* Python
* LangChain
* Google Gemini API
* FAISS
* python-dotenv

---

## Example Use Cases

* Arabic knowledge assistants
* Document Q&A systems
* Educational tools
* Internal company knowledge search

---

## arabic.txt (example content)

Create a simple knowledge file. You can replace it with your own text.

```
الذكاء الاصطناعي هو مجال من مجالات علوم الحاسوب يهدف إلى إنشاء أنظمة قادرة على محاكاة الذكاء البشري.

يشمل الذكاء الاصطناعي عدة مجالات مثل:
- تعلم الآلة
- معالجة اللغة الطبيعية
- الرؤية الحاسوبية

يستخدم الذكاء الاصطناعي في العديد من التطبيقات مثل المساعدات الصوتية، أنظمة التوصية، وتحليل البيانات.
```

---

## requirements.txt

```
langchain
langchain-core
langchain-community
langchain-google-genai
langchain-text-splitters
google-generativeai
faiss-cpu
python-dotenv
```

---

## .env (example)

Create this file locally (do not upload to GitHub):

```
GOOGLE_API_KEY=your_google_api_key_here
```

---

## rag_app.py

Use your provided code exactly as the main script.

(Keep your current implementation.)

---

## .gitignore (recommended)

```
.env
venv/
__pycache__/
*.pyc
```
