import streamlit as st

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# Streamlit Configuration
# ============================================================

st.set_page_config(layout="wide")
st.title("My Local Chatbot")


# ============================================================
# Sidebar Settings
# ============================================================

st.sidebar.header("Settings")

MODEL = st.sidebar.selectbox(
    "Choose a Model",
    ["llama3.2", "deepseek-r1:1.5b"],
    index=0
)

MAX_HISTORY = st.sidebar.number_input(
    "Max History",
    min_value=1,
    max_value=10,
    value=2
)

CONTEXT_SIZE = st.sidebar.number_input(
    "Context Size",
    min_value=1024,
    max_value=16384,
    value=8192,
    step=1024
)


# ============================================================
# Session State
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if (
    "prev_context_size" not in st.session_state
    or st.session_state.prev_context_size != CONTEXT_SIZE
):
    st.session_state.prev_context_size = CONTEXT_SIZE


# ============================================================
# Initialize Ollama LLM
# ============================================================

llm = ChatOllama(
    model=MODEL,
    temperature=0,
    num_ctx=CONTEXT_SIZE,
    streaming=True
)


# ============================================================
# Initialize Ollama Embeddings
# ============================================================

embeddings = OllamaEmbeddings(
    model="mxbai-embed-large"
)


# ============================================================
# Initialize ChromaDB
# ============================================================

persist_directory = "./chroma_db"

vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings
)


# ============================================================
# Create Retriever
# ============================================================

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5
    }
)


# ============================================================
# RAG Prompt
# ============================================================

prompt_template = ChatPromptTemplate.from_template(
    """You are a helpful assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:"""
)


# ============================================================
# Display Chat History
# ============================================================

for msg in st.session_state.chat_history:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ============================================================
# Trim Chat History
# ============================================================

def trim_history():

    max_messages = MAX_HISTORY * 2

    if len(st.session_state.chat_history) > max_messages:

        st.session_state.chat_history = (
            st.session_state.chat_history[-max_messages:]
        )


# ============================================================
# Handle User Input
# ============================================================

if user_prompt := st.chat_input("Say something"):

    # --------------------------------------------------------
    # Add user message to history
    # --------------------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    trim_history()


    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        response_container = st.empty()

        # Retrieve relevant documents
        retrieved_docs = retriever.invoke(user_prompt)

        if not retrieved_docs:

            full_response = "No relevant documents found."

        else:

            # ------------------------------------------------
            # Combine retrieved documents into context
            # ------------------------------------------------

            context = "\n\n".join(
                doc.page_content
                for doc in retrieved_docs
            )

            # ------------------------------------------------
            # Create prompt
            # ------------------------------------------------

            messages = prompt_template.invoke(
                {
                    "context": context,
                    "question": user_prompt
                }
            )

            # ------------------------------------------------
            # Invoke LLM
            # ------------------------------------------------

            response = llm.invoke(messages)

            full_response = response.content

        # ----------------------------------------------------
        # Display response
        # ----------------------------------------------------

        response_container.markdown(full_response)

    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )

    trim_history()
