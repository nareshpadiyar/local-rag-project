# Data Ingestion - Private documents are loaded using the appropriate LangChain document loader.
from pathlib import Path

from langchain_community.document_loaders import (
    CSVLoader,
    PyPDFLoader,
    TextLoader,
    BSHTMLLoader,
    Docx2txtLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    UnstructuredMarkdownLoader
)


def CSVLoaderFunc(files):
    docs = []
    for file in files:
        docs.extend(CSVLoader(file).load())
    return docs


def DOCLoader(files):
    docs = []
    for file in files:
        # Legacy .doc files need the unstructured loader.
        if Path(file).suffix.lower() == ".doc":
            loader = UnstructuredWordDocumentLoader(file)
        else:
            loader = Docx2txtLoader(file)
        docs.extend(loader.load())
    return docs


def HTMLLoader(files):
    docs = []
    for file in files:
        docs.extend(BSHTMLLoader(file).load())
    return docs


def JSONLoaderFunc(files):
    docs = []
    for file in files:
        # Preserve the original JSON content as text.
        docs.extend(TextLoader(file, encoding="utf-8").load())
    return docs


def MDLoader(files):
    docs = []
    for file in files:
        docs.extend(UnstructuredMarkdownLoader(file).load())
    return docs


def PDFLoader(files):
    docs = []
    for file in files:
        docs.extend(PyPDFLoader(file).load())
    return docs


def PPTLoader(files):
    docs = []
    for file in files:
        docs.extend(UnstructuredPowerPointLoader(file).load())
    return docs


def SQLLoader(files):
    docs = []
    for file in files:
        # SQL files are loaded as text, including queries and schemas.
        docs.extend(TextLoader(file, encoding="utf-8").load())
    return docs


def TXTLoader(files):
    docs = []
    for file in files:
        docs.extend(TextLoader(file, encoding="utf-8").load())
    return docs


def XLSLoader(files):
    docs = []
    for file in files:
        docs.extend(UnstructuredExcelLoader(file).load())
    return docs



# Iterate through each private data source category and use list comprehension to store its corresponding documents.
csv_files  = [str(f) for f in Path("datasource/CSV").rglob("*.csv")]

doc_files  = [
    str(f) for f in Path("datasource/DOC").rglob("*")
    if f.is_file() and f.suffix.lower() in [".doc", ".docx"]
]

html_files = [
    str(f) for f in Path("datasource/HTML").rglob("*")
    if f.is_file() and f.suffix.lower() in [".html", ".htm"]
]

json_files = [str(f) for f in Path("datasource/JSON").rglob("*.json")]

md_files   = [str(f) for f in Path("datasource/MD").rglob("*.md")]

pdf_files  = [str(f) for f in Path("datasource/PDF").rglob("*.pdf")]

ppt_files = [
    str(f) for f in Path("datasource/PPT").rglob("*")
    if f.is_file() and f.suffix.lower() in [".ppt", ".pptx"]
]

sql_files = [str(f) for f in Path("datasource/SQL").rglob("*.sql")]

txt_files = [str(f) for f in Path("datasource/TXT").rglob("*.txt")]

xls_files = [
    str(f) for f in Path("datasource/XLS").rglob("*")
    if f.is_file() and f.suffix.lower() in [".xls", ".xlsx"]
]


# Load documents
csv_docs = CSVLoaderFunc(csv_files)
doc_docs = DOCLoader(doc_files)
html_docs = HTMLLoader(html_files)
json_docs = JSONLoaderFunc(json_files)
md_docs = MDLoader(md_files)
pdf_docs = PDFLoader(pdf_files)
ppt_docs = PPTLoader(ppt_files)
sql_docs = SQLLoader(sql_files)
txt_docs = TXTLoader(txt_files)
xls_docs = XLSLoader(xls_files)


# Combine all loaded documents for downstream processing
all_docs = (csv_docs + doc_docs + html_docs + json_docs + md_docs + pdf_docs + ppt_docs + sql_docs + txt_docs + xls_docs)
print(f"Total documents loaded: {len(all_docs)}")


# Text Splitting - Large documents are divided into smaller chunks to improve retrieval accuracy.
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

split_documents = text_splitter.split_documents(all_docs)

print(f"Total documents: {len(all_docs)}")
print(f"Total chunks: {len(split_documents)}")


# Embeddings - Each document chunk is converted into a numerical vector using an Ollama embedding model. The generated embeddings are stored in ChromaDB.
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Initialize Ollama Embeddings
embeddings = OllamaEmbeddings(
    model="mxbai-embed-large"
)

# Set directory for persistent storage
persist_directory = "./chroma_db"

# Create and persist ChromaDB vector store
vectorstore = Chroma.from_documents(
    documents=split_documents,
    embedding=embeddings,
    persist_directory=persist_directory
)

print("✅ Data successfully stored in ChromaDB!")

# Reload the vector store for retrieval
vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings
)

print("🔄 ChromaDB reloaded successfully!")