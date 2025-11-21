import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()


class NutritionSchema(BaseModel):
    calories: str = Field(description="e.g., '500 kcal'")
    protein: str = Field(description="e.g., '30g'")
    carbs: str = Field(description="e.g., '40g'")
    fats: str = Field(description="e.g., '15g'")


class RecipeSchema(BaseModel):
    dish_name: str = Field(description="Name of the dish")
    ingredients: List[str] = Field(description="List of ingredients with quantities")
    instructions: List[str] = Field(description="Step-by-step cooking instructions")
    # Change type from 'dict' to 'NutritionSchema'
    nutrition: NutritionSchema = Field(description="Nutritional content")
    tips: List[str] = Field(description="3 helpful cooking tips")

def generate_recipe_chain(query: str):
    api_key = os.getenv("GEMINI_API_KEY")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.5
    )
    
    structured_llm = llm.with_structured_output(RecipeSchema)

    prompt = PromptTemplate(
        template="""
        You are a master chef. Create a detailed recipe based on this request: "{query}".
        
        REQUIREMENTS:
        - Ensure nutritional data (calories, protein) is accurate.
        - Be beginner-friendly.
        """,
        input_variables=["query"]
    )

    chain = prompt | structured_llm
    
    try:
        return chain.invoke({"query": query})
    except Exception as e:
        print(f"LLM Error: {e}")
        return None