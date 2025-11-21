from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.services.llm_service import generate_recipe_chain
from backend.services.image_service import generate_dish_image
from backend.services.video_service import get_youtube_link
import base64

app = FastAPI(title="AI Recipe Engine")

# Enable CORS (Cross-Origin Resource Sharing) so Streamlit can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecipeRequest(BaseModel):
    query: str

@app.post("/generate")
async def generate_recipe(request: RecipeRequest):
    # 1. Generate Text (LLM)
    recipe_data = generate_recipe_chain(request.query)
    
    if not recipe_data:
        raise HTTPException(status_code=500, detail="Failed to generate recipe text")

    # 2. Generate Image
    image_bytes = generate_dish_image(recipe_data.dish_name)
    image_b64 = None
    if image_bytes:
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')

    # 3. Get Video
    video_url = get_youtube_link(recipe_data.dish_name)

    return {
        "recipe": recipe_data.dict(),
        "image_b64": image_b64,
        "video_url": video_url
    }