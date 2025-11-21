import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import io

load_dotenv()

def generate_dish_image(dish_name: str):
    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        print("Error: HF_API_KEY is missing.")
        return None

    # Initialize the official client
    client = InferenceClient(token=api_key)
    
    # Prompt Engineering for better food results
    prompt = f"Professional food photography of {dish_name}, high resolution, appetizing, soft studio lighting, 4k, culinary magazine style, top-down view"

    try:
        # The client handles the URL and API calls automatically
        # FLUX.1-dev is excellent, but if it times out on the free tier, 
        # try "stabilityai/stable-diffusion-xl-base-1.0"
        image = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-dev"
        )
        
        # Converting PIL Image to Bytes so we can send it to the frontend
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    except Exception as e:
        print(f"Image Generation Error: {e}")
        return None