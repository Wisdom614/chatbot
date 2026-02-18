import streamlit as st
from transformers import pipeline
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import io
import datetime
import random
import time

# Page configuration
st.set_page_config(
    page_title="Besong Wisdom AI Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for your branding
st.markdown(f"""
<style>
    /* Main container styling */
    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }}
    
    /* Custom header for Besong Wisdom */
    .wisdom-header {{
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    /* Your website banner */
    .website-banner {{
        background-color: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        border: 2px solid #4ECDC4;
    }}
    
    /* Custom card styling */
    .feature-card {{
        background-color: rgba(255,255,255,0.15);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    /* Success message styling */
    .success-message {{
        background: linear-gradient(90deg, #00b09b, #96c93d);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state for history
if 'text_history' not in st.session_state:
    st.session_state.text_history = []
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# Header with your name
st.markdown(f"""
<div class="wisdom-header">
    🎨 Besong Wisdom AI Studio 🤖
</div>
<div class="website-banner">
    🌐 <a href="https://besongwisdom.online" target="_blank" style="color: white; text-decoration: none; font-size: 1.2em;">
        besongwisdom.online
    </a> 🌐
</div>
""", unsafe_allow_html=True)

# Sidebar with your info
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/4ECDC4/FFFFFF?text=Besong+Wisdom+AI", use_column_width=True)
    
    st.markdown("## 👋 Welcome!")
    st.markdown(f"""
    <div class="feature-card">
        <h3 style='color: #FFD93D;'>Created by Besong Wisdom</h3>
        <p>📍 AI Developer & Creative Technologist</p>
        <p>🚀 Exploring the frontiers of AI</p>
        <p>💡 Turning ideas into intelligent applications</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model selection
    st.markdown("### ⚙️ Settings")
    
    # Temperature slider for creativity
    creativity = st.slider(
        "🎨 Creativity Level",
        min_value=0.1,
        max_value=1.5,
        value=0.8,
        step=0.1,
        help="Lower = more predictable, Higher = more creative"
    )
    
    # Max length for text
    max_length = st.slider(
        "📏 Story Length",
        min_value=50,
        max_value=500,
        value=200,
        step=50
    )
    
    # Image settings
    image_steps = st.slider(
        "🖼️ Image Quality Steps",
        min_value=10,
        max_value=50,
        value=30,
        step=5,
        help="More steps = better quality but slower"
    )
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📊 Today's Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Text Generations", len(st.session_state.text_history))
    with col2:
        st.metric("Images Created", len(st.session_state.image_history))
    
    # Clear history button
    if st.button("🧹 Clear History"):
        st.session_state.text_history = []
        st.session_state.image_history = []
        st.success("History cleared!")
        st.rerun()

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 AI Storyteller", 
    "🎨 AI Image Generator",
    "🖼️ My Gallery",
    "ℹ️ About Me"
])

# Tab 1: AI Storyteller
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ✍️ Write Your Story Prompt")
        
        # Example prompts
        example_prompts = [
            "A magical adventure in a chocolate factory",
            "A robot who learns to dance",
            "The day animals could talk",
            "A journey to the center of the earth",
            "My pet dinosaur's first day at school"
        ]
        
        selected_example = st.selectbox(
            "Need inspiration? Try an example:",
            ["Choose an example..."] + example_prompts
        )
        
        # Text input
        prompt = st.text_area(
            "Your story idea:",
            value=selected_example if selected_example != "Choose an example..." else "",
            height=100,
            placeholder="Once upon a time..."
        )
        
        # Generate button
        if st.button("🚀 Generate Story", type="primary", use_container_width=True):
            if prompt:
                with st.spinner("🤔 Besong's AI is crafting your story..."):
                    try:
                        # Load text generation model
                        @st.cache_resource
                        def load_text_model():
                            return pipeline('text-generation', model='gpt2')
                        
                        generator = load_text_model()
                        
                        # Progress bar for fun
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.02)
                            progress_bar.progress(i + 1)
                        
                        # Generate
                        result = generator(
                            prompt,
                            max_length=max_length,
                            temperature=creativity,
                            do_sample=True,
                            pad_token_id=50256
                        )
                        
                        progress_bar.empty()
                        
                        # Display result
                        story = result[0]['generated_text']
                        
                        st.markdown("### 📖 Your Magical Story:")
                        st.markdown(f"""
                        <div style="background-color: rgba(255,255,255,0.1); padding: 25px; border-radius: 15px; font-size: 1.1em; line-height: 1.6;">
                            {story}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Save to history
                        st.session_state.text_history.append({
                            'prompt': prompt,
                            'story': story,
                            'time': datetime.datetime.now()
                        })
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Story",
                            data=story,
                            file_name=f"wisdom_story_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                        
                        # Celebrate!
                        st.balloons()
                        st.markdown('<div class="success-message">✨ Story created successfully!</div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Oops! {str(e)}")
            else:
                st.warning("Please enter a story prompt!")
    
    with col2:
        st.markdown("### 💡 Pro Tips")
        st.info("""
        **Make your stories better:**
        - Be specific about characters
        - Describe the setting
        - Add emotions
        - Include dialogue
        """)
        
        st.markdown("### 🎯 Recent Stories")
        for item in reversed(st.session_state.text_history[-5:]):
            with st.expander(f"📝 {item['prompt'][:30]}..."):
                st.write(item['story'][:100] + "...")

# Tab 2: AI Image Generator
with tab2:
    st.markdown("### 🎨 Create Amazing Images with AI")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Describe Your Image")
        
        image_prompt = st.text_area(
            "What would you like to see?",
            height=150,
            placeholder="Example: A futuristic city with rainbow buildings and flying cars, digital art style",
            key="image_prompt"
        )
        
        # Style selection
        style = st.selectbox(
            "Choose a style:",
            ["Photorealistic", "Anime", "Oil Painting", "Watercolor", "Sketch", "3D Render", "Pixel Art"]
        )
        
        # Size selection
        size = st.selectbox(
            "Image size:",
            ["512x512", "768x768", "1024x1024"]
        )
        
        if st.button("🎨 Generate Image", type="primary", use_container_width=True):
            if image_prompt:
                with st.spinner("🎨 Besong's AI is painting your masterpiece..."):
                    try:
                        # For demo purposes, we'll create a placeholder
                        # In production, you'd use actual Stable Diffusion
                        
                        # Simulate image generation progress
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i in range(image_steps):
                            time.sleep(0.1)
                            progress_bar.progress(i + 1)
                            status_text.text(f"Creating magic... Step {i+1}/{image_steps}")
                        
                        # Create a colorful gradient image as placeholder
                        # (Replace this with actual Stable Diffusion in production)
                        from PIL import Image, ImageDraw, ImageFont
                        
                        # Create a cool gradient image
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
                        
                        # Add text overlay
                        try:
                            font = ImageFont.truetype("arial.ttf", 30)
                        except:
                            font = ImageFont.load_default()
                        
                        draw.text((50, 250), f"Besong Wisdom AI", fill="white", font=font)
                        draw.text((50, 300), f"Style: {style}", fill="white", font=font)
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Display the image
                        st.image(img, caption=f"Generated: {image_prompt[:50]}...", use_column_width=True)
                        
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
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            label="💾 Download Image",
                            data=byte_im,
                            file_name=f"wisdom_ai_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                            mime="image/png"
                        )
                        
                        st.balloons()
                        st.success("🎉 Image created successfully!")
                        
                    except Exception as e:
                        st.error(f"Image generation error: {str(e)}")
            else:
                st.warning("Please describe what image you want to create!")
    
    with col2:
        st.markdown("#### 🖼️ Style Examples")
        
        # Create style examples
        for style_name in ["Photorealistic", "Anime", "Oil Painting"][:3]:
            with st.expander(f"✨ {style_name} Style"):
                st.markdown(f"""
                **Try prompts like:**
                - "A {style_name.lower()} portrait of a cat wearing sunglasses"
                - "Mountain landscape in {style_name.lower()} style"
                - "Fantasy castle, {style_name.lower()} artwork"
                """)

# Tab 3: Gallery
with tab3:
    st.markdown("### 🖼️ Besong's AI Gallery")
    
    if not st.session_state.image_history and not st.session_state.text_history:
        st.info("✨ Your gallery is empty. Create some magic in the other tabs!")
    else:
        # Show image gallery
        if st.session_state.image_history:
            st.markdown("#### 🎨 Image Creations")
            
            # Create grid layout for images
            cols = st.columns(3)
            for idx, item in enumerate(reversed(st.session_state.image_history[-9:])):
                with cols[idx % 3]:
                    st.image(item['image'], caption=f"{item['prompt'][:30]}...", use_column_width=True)
                    st.caption(f"🕐 {item['time'].strftime('%H:%M')}")
        
        # Show text history
        if st.session_state.text_history:
            st.markdown("#### 📝 Story Collection")
            for item in reversed(st.session_state.text_history[-5:]):
                with st.expander(f"📖 {item['prompt']}"):
                    st.write(item['story'])
                    st.caption(f"Created: {item['time'].strftime('%Y-%m-%d %H:%M')}")

# Tab 4: About Me
with tab4:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #667eea, #764ba2); padding: 30px; border-radius: 20px; text-align: center;">
            <h1 style="color: white; font-size: 3em;">👨‍💻</h1>
            <h2 style="color: white;">Besong Wisdom</h2>
            <p style="color: #FFD93D;">AI Developer & Creative Technologist</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### 🚀 About Besong Wisdom
        
        Welcome to my AI Studio! I'm passionate about making AI accessible and fun for everyone.
        
        **🎯 What I Do:**
        - Build intelligent applications
        - Create AI-powered creative tools
        - Make technology fun and engaging
        
        **💡 My Mission:**
        To democratize AI and help people unleash their creativity through technology.
        
        **🌟 Featured Project:**
        This AI Studio combines text generation and image creation in one beautiful interface.
        
        ### 📬 Connect With Me
        """)
        
        # Social links
        st.markdown("""
        - 🌐 **Website:** [besongwisdom.online](https://besongwisdom.online)
        - 📧 **Email:** contact@besongwisdom.online
        - 💼 **LinkedIn:** [Besong Wisdom](https://linkedin.com/in/besongwisdom)
        - 🐦 **Twitter:** [@besongwisdom](https://twitter.com/besongwisdom)
        """)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: white; padding: 20px;">
    🚀 Created with ❤️ by <a href="https://besongwisdom.online" style="color: #FFD93D;">Besong Wisdom</a> | 
    © 2026 All rights reserved | 
    Powered by AI Magic ✨
</div>
""", unsafe_allow_html=True)