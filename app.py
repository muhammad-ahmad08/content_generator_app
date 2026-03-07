import streamlit as st
from generator import generate_content

st.title("AI Content Generator")

topic = st.text_input("Enter Topic")
tone = st.selectbox("Tone", ["Professional", "Casual", "Marketing"])

if st.button("Generate Content"):
    output = generate_content(topic, tone)
    st.write(output)