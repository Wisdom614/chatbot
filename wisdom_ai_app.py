import streamlit as st
import torch
from PIL import Image, ImageDraw, ImageFont
import datetime
import time
import io

# Page configuration
st.set_page_config(
    page_title="Besong Wisdom AI Studio",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS (keep your existing CSS)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .wisdom-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .website-banner {
        background-color: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="wisdom-header">
    🎨 Besong Wisdom AI Studio 🤖
</div>
<div class="website-banner">
    🌐 <a href="https://besongwisdom.online" target="_blank" style="color: white; text-decoration: none; font-size: 1.2em;">
        besongwisdom.online
    </a> 🌐
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'text_history' not in st.session_state:
    st.session_state.text_history = []
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# Sidebar
with st.sidebar:
    st.markdown("## 👋 Welcome to Besong's AI Studio!")
    
    # Model selection with cloud-optimized options
    st.markdown("### ⚙️ Settings")
    
    # Text generation settings
    use_real_ai = st.checkbox("🚀 Enable Real AI (May be slower)", value=False)
    
    creativity = st.slider("Creativity Level", 0.1, 1.5, 0.8)
    max_length = st.slider("Story Length", 50, 300, 150)
    
    # Stats
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.metric("Stories Created", len(st.session_state.text_history))
    st.metric("Images Created", len(st.session_state.image_history))

# Load AI models only when needed (with error handling)
@st.cache_resource
def load_text_model():
    try:
        from transformers import pipeline
        return pipeline('text-generation', model='gpt2', device_map="auto" if torch.cuda.is_available() else None)
    except Exception as e:
        st.warning(f"Could not load AI model: {e}")
        return None

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Story Generator", "🎨 Image Creator", "🖼️ Gallery", "ℹ️ About"])

# Tab 1: Story Generator
with tab1:
    st.markdown("### 📝 AI Story Generator")
    
    prompt = st.text_area("What story would you like to tell?", 
                          placeholder="Once upon a time...",
                          height=100)
    
    if st.button("✨ Generate Story", type="primary"):
        if prompt:
            with st.spinner("Creating your story..."):
                if use_real_ai:
                    # Try to use real AI
                    generator = load_text_model()
                    if generator:
                        try:
                            result = generator(prompt, 
                                             max_length=max_length,
                                             temperature=creativity,
                                             do_sample=True)
                            story = result[0]['generated_text']
                        except:
                            story = f"{prompt}\n\nOnce upon a time, in a world of imagination, your story began to unfold. The AI is taking a short break, but here's a starter for you!"
                    else:
                        story = f"{prompt}\n\n✨ Your story continues to unfold in the most magical way possible. The characters come alive, the plot thickens, and adventure awaits!"
                else:
                    # Demo mode with template stories
                    templates = [
                        f"{prompt} And so began the most amazing adventure anyone had ever seen. The hero, brave and true, faced challenges with courage and wit.",
                        f"{prompt} In a land far away, where magic was real and dreams came true, our story begins with a twist of fate.",
                        f"{prompt} Little did anyone know that this was just the beginning of something extraordinary."
                    ]
                    import random
                    story = random.choice(templates)
                
                # Display story
                st.markdown("### Your Story:")
                st.markdown(f"<div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>{story}</div>", unsafe_allow_html=True)
                
                # Save to history
                st.session_state.text_history.append({
                    'prompt': prompt,
                    'story': story,
                    'time': datetime.datetime.now()
                })
                
                # Download button
                st.download_button("📥 Download Story", story, 
                                 file_name=f"story_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
                
                st.balloons()
        else:
            st.warning("Please enter a story prompt!")

# Tab 2: Image Creator
with tab2:
    st.markdown("### 🎨 AI Image Creator")
    
    image_prompt = st.text_area("Describe the image you want to create:",
                                placeholder="A magical forest with glowing trees and fairy houses",
                                height=100,
                                key="img_prompt")
    
    style = st.selectbox("Choose style:", ["Fantasy", "Sci-Fi", "Nature", "Abstract", "Cartoon"])
    
    if st.button("🎨 Create Image", type="primary"):
        if image_prompt:
            with st.spinner("Painting your masterpiece..."):
                # Create a custom image with text
                img = Image.new('RGB', (512, 512), color=(73, 109, 137))
                draw = ImageDraw.Draw(img)
                
                # Add some simple shapes
                draw.rectangle([100, 100, 400, 400], fill=(200, 200, 200, 50))
                draw.ellipse([200, 200, 300, 300], fill=(255, 215, 0))
                
                # Add text
                try:
                    draw.text((50, 450), f"Besong Wisdom AI", fill=(255, 255, 255))
                    draw.text((50, 470), f"Style: {style}", fill=(255, 255, 255))
                    draw.text((50, 490), f"{image_prompt[:30]}...", fill=(255, 255, 255))
                except:
                    pass
                
                # Display image
                st.image(img, caption=f"Created for: {image_prompt}", use_column_width=True)
                
                # Save to history
                st.session_state.image_history.append({
                    'prompt': image_prompt,
                    'style': style,
                    'image': img,
                    'time': datetime.datetime.now()
                })
                
                # Download button
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                st.download_button("💾 Download Image", buf.getvalue(),
                                 file_name=f"image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                 mime="image/png")
                
                st.success("Image created!")
        else:
            st.warning("Please describe your image!")

# Tab 3: Gallery
with tab3:
    st.markdown("### 🖼️ Your Gallery")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Recent Stories")
        for item in st.session_state.text_history[-5:]:
            with st.expander(f"📖 {item['prompt'][:30]}..."):
                st.write(item['story'])
    
    with col2:
        st.markdown("#### 🎨 Recent Images")
        cols = st.columns(2)
        for idx, item in enumerate(st.session_state.image_history[-4:]):
            with cols[idx % 2]:
                st.image(item['image'], caption=item['prompt'][:20], use_column_width=True)

# Tab 4: About
with tab4:
    st.markdown("""
    ### 👨‍💻 Besong Wisdom
    
    Welcome to my AI Studio! I create magical experiences with artificial intelligence.
    
    **🚀 Features:**
    - AI Story Generation
    - Creative Image Making
    - Personal Gallery
    
    **🌐 Visit my website:** [besongwisdom.online](https://besongwisdom.online)
    
    **📧 Contact:** contact@besongwisdom.online
    """)

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align: center'>Created with ❤️ by <a href='https://besongwisdom.online'>Besong Wisdom</a> | © 2024</div>", unsafe_allow_html=True)