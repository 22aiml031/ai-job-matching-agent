import streamlit as st
from job_matching_agent.embeddings.embedding_model import EmbeddingGenerator

st.title("Test Embedding Generator")

text_input = st.text_area("Enter text to generate embedding:")

if st.button("Generate Embedding"):
    if text_input:
        generator = EmbeddingGenerator()
        embedding = generator.generate_single(text_input)
        st.write("Embedding:", embedding)
    else:
        st.warning("Please enter some text.")
