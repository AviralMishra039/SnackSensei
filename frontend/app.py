import streamlit as st
import requests
import base64


API_URL = "https://aiviralx-snack-sensei-backend.hf.space/generate"

st.set_page_config(page_title="Snack Sensei", layout="wide")

st.title("Snack Sensei 👨‍🍳")
st.caption("Powered by Gemini, LangChain, FastAPI & Hugging Face")

with st.sidebar:
    st.header("Input")
    user_input = st.text_area("What are you craving?", height=150)
    generate_btn = st.button("Create Recipe", type="primary")

if generate_btn and user_input:
    with st.spinner("🧠 Orchestrating Recipe (LLM + Image Gen + Video Search)..."):
        try:
            # Note: When running locally, change API_URL to http://127.0.0.1:8000/generate
            response = requests.post(API_URL, json={"query": user_input})
            
            if response.status_code == 200:
                data = response.json()
                recipe = data['recipe']
                
                # Layout
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.subheader(recipe['dish_name'])
                    # Display Image
                    if data['image_b64']:
                        st.image(base64.b64decode(data['image_b64']), use_container_width=True)
                    else:
                        st.warning("Image generation failed or timed out.")
                    
                    # Display Nutrition
                    st.info(f"**Calories:** {recipe['nutrition'].get('calories', 'N/A')} | **Protein:** {recipe['nutrition'].get('protein', 'N/A')}")

                with col2:
                    # Instructions & Ingredients
                    st.markdown("### 🥕 Ingredients")
                    for item in recipe['ingredients']:
                        st.markdown(f"- {item}")
                        
                    st.markdown("### 🍳 Instructions")
                    for idx, step in enumerate(recipe['instructions']):
                        st.markdown(f"**{idx+1}.** {step}")
                
                # Video & Tips
                st.divider()
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("### 💡 Chef's Tips")
                    for tip in recipe['tips']:
                        st.success(tip)
                with c2:
                    st.markdown("### 📺 Tutorial")
                    if data['video_url']:
                        st.video(data['video_url'])
                    else:
                        st.write("No video available.")

            else:
                st.error(f"Backend Error: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to Backend. If running locally, make sure FastAPI is running.")