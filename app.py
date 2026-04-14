import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

st.title("📚 DPDP + Banking Laws Chatbot ")

# Use caching so models and DB only load once, not on every user interaction
@st.cache_resource
def load_rag_components():
    # Load embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load DB (Ensure you have a folder named 'db' in your working directory)
    db = FAISS.load_local("db", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # Load model
    pipe = pipeline(
        "text-generation",
        model="gpt2",
        max_new_tokens=150,
        pad_token_id=50256 # Added to suppress a common warning with GPT-2
    )
    
    return retriever, pipe

# Load components
try:
    retriever, pipe = load_rag_components()
except Exception as e:
    st.error(f"Failed to load the database or models: {e}")
    st.stop()

# User Input
query = st.text_input("Ask your question:")

# Execution block: Only runs when the user submits a query
if query:
    with st.spinner("Searching documents and generating response..."):
        # 1. Retrieve documents based on the query
        docs = retriever.invoke(query)

        # 2. Extract and combine the text context
        context = " ".join([doc.page_content for doc in docs])

        # 3. Build the prompt
        prompt = f"""Answer the question based on the context below.

Context:
{context}

Question:
{query}

Answer:
"""

        # 4. Generate the result
        result = pipe(prompt)[0]["generated_text"]

        # 5. Clean up the output 
        # GPT-2 tends to repeat the prompt, so we split the string to only show the generated answer
        try:
            final_answer = result.split("Answer:")[1].strip()
        except IndexError:
            final_answer = result # Fallback just in case

        # Display results
        st.write("### Answer:")
        st.write(final_answer)
        
        # Optional: Add an expander to let the user see the retrieved legal text
        with st.expander("View Retrieved Context"):
            st.write(context)