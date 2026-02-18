import streamlit as st
import datetime
import random
from PIL import Image, ImageDraw
import io

# Page configuration
st.set_page_config(
    page_title="Besong Wisdom AI Studio",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS
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
    .feature-card {
        background-color: rgba(255,255,255,0.15);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'text_history' not in st.session_state:
    st.session_state.text_history = []
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# Header
st.markdown("""
<div class="wisdom-header">
    🎨 Besong Wisdom AI Studio 🤖
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 👋 Welcome!")
    st.markdown("""
    <div class="feature-card">
        <h3>Created by Besong Wisdom</h3>
        <p>📍 AI Developer</p>
        <p>🌐 besongwisdom.online</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings
    creativity = st.slider("Creativity Level", 0.1, 1.5, 0.8)
    max_length = st.slider("Story Length", 50, 300, 150)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 AI Storyteller", "🎨 AI Image Generator", 
    "🖼️ Gallery", "ℹ️ About"
])

# Tab 1: AI Storyteller (Demo Mode)
with tab1:
    st.markdown("### ✍️ AI Story Generator")
    
    prompt = st.text_area("Your story idea:", 
                         "A magical adventure in a chocolate factory",
                         height=100)
    
    if st.button("Generate Story", type="primary"):
        with st.spinner("Creating your story..."):
            # Demo stories based on keywords
            demo_stories = {
                "magic": "In a world where magic flowed like water, young Elara discovered she could talk to animals. The squirrels became her spies, and the birds her messengers...",
                "adventure": "Captain Zara's spaceship malfunctioned, crash-landing on an unknown planet. The purple trees glowed in the twilight as strange creatures approached...",
                "robot": "Beeper the robot wasn't like other robots. He dreamed of painting sunsets and writing poetry. His circuits hummed with creativity...",
                "default": "Once upon a time, in a land far away, there lived a curious child who loved to ask questions. Every answer led to more questions, and every question led to new adventures..."
            }
            
            story = demo_stories.get("default")
            for key in demo_stories:
                if key in prompt.lower():
                    story = demo_stories[key]
                    break
            
            # Add some generated text
            story += f"\n\n{'. '.join([f'And then {random.choice(["something magical", "a surprise", "an adventure", "a mystery"])} happened' for _ in range(5)])}..."
            
            st.markdown(f"**Your Story:**\n\n{story}")
            
            # Save to history
            st.session_state.text_history.append({
                'prompt': prompt,
                'story': story,
                'time': datetime.datetime.now()
            })
            
            st.balloons()

# Tab 2: AI Image Generator (Demo Mode)
with tab2:
    st.markdown("### 🎨 AI Image Creator")
    
    image_prompt = st.text_area("Describe your image:", 
                               "A beautiful sunset over a futuristic city",
                               height=100)
    
    style = st.selectbox("Style:", ["Fantasy", "Sci-Fi", "Nature", "Abstract"])
    
    if st.button("Generate Image", type="primary"):
        with st.spinner("Painting your image..."):
            # Create a simple gradient image as placeholder
            img = Image.new('RGB', (512, 512))
            draw = ImageDraw.Draw(img)
            
            # Create gradient
            for i in range(512):
                color = (
                    int(255 * (i/512)),
                    int(100 + 155 * (i/512)),
                    int(200 - 100 * (i/512))
                )
                draw.line([(i, 0), (i, 512)], fill=color, width=1)
            
            # Add text
            draw.text((50, 250), f"Besong Wisdom AI", fill="white")
            draw.text((50, 300), f"Style: {style}", fill="white")
            draw.text((50, 350), f"Prompt: {image_prompt[:30]}...", fill="white")
            
            st.image(img, caption=f"Generated Image - {style} Style")
            
            # Save to history
            st.session_state.image_history.append({
                'prompt': image_prompt,
                'style': style,
                'image': img,
                'time': datetime.datetime.now()
            })
            
            st.balloons()

# Tab 3: Gallery
with tab3:
    st.markdown("### 🖼️ Your Gallery")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Recent Stories**")
        for item in st.session_state.text_history[-3:]:
            with st.expander(f"📝 {item['prompt'][:30]}..."):
                st.write(item['story'][:150] + "...")
    
    with col2:
        st.markdown("**Recent Images**")
        for item in st.session_state.image_history[-3:]:
            st.image(item['image'], caption=item['prompt'][:30], width=200)

# Tab 4: About
with tab4:
    st.markdown("""
    ### About Besong Wisdom
    
    Welcome to my AI Studio! I'm passionate about making AI accessible and fun.
    
    **Connect with me:**
    - 🌐 Website: [besongwisdom.online](https://besongwisdom.online)
    - 📧 Email: contact@besongwisdom.online
    
    **About this app:**
    This is a demo version of my AI Studio. The full version with real AI models 
    requires more computational resources.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 20px;">
    🚀 Created with ❤️ by <a href="https://besongwisdom.online" style="color: #FFD93D;">Besong Wisdom</a>
</div>
""", unsafe_allow_html=True)