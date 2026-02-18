import streamlit as st
from transformers import pipeline
import time

st.set_page_config(page_title="AI Fun Generator", page_icon="🤖")

# Load model
@st.cache_resource
def load_model():
    return pipeline('text-generation', model='gpt2')

st.title("🤖 AI Text Generator for Kids")
st.markdown("### Let's create some fun stories together!")

# Sidebar with controls
with st.sidebar:
    st.header("Settings")
    max_length = st.slider("How long should the story be?", 50, 300, 150)
    temperature = st.slider("How creative? (0 = boring, 1 = crazy)", 0.1, 1.5, 0.8)
    
    st.markdown("---")
    st.markdown("### About")
    st.info("This AI helps you generate fun stories! Just type a prompt and see what happens!")

# Main area
prompt = st.text_area("✨ Type your story starter here:", 
                      "Once upon a time in a magical forest...",
                      height=100)

if st.button("🚀 Generate Story", type="primary"):
    if prompt:
        with st.spinner("AI is thinking... 🤔"):
            # Load model and generate
            generator = load_model()
            
            # Show progress bar for fun
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Generate text
            result = generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                do_sample=True
            )
            
            progress_bar.empty()
            
            # Display result in a nice box
            st.markdown("### 📝 Your Generated Story:")
            st.markdown(f'<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">{result[0]["generated_text"]}</div>', 
                       unsafe_allow_html=True)
            
            # Download button
            st.download_button(
                label="📥 Download Story",
                data=result[0]['generated_text'],
                file_name="my_story.txt",
                mime="text/plain"
            )
    else:
        st.warning("Please enter a prompt first!")

# Fun facts in expander
with st.expander("🎯 Fun Facts about AI"):
    st.write("""
    - AI learns like you do - from examples!
    - This AI was trained on millions of books and websites
    - AI can write poems, stories, and even jokes!
    - Sometimes AI makes silly mistakes - that's part of the fun!
    """)