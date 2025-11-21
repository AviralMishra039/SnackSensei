import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def get_youtube_link(dish_name: str):
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q=f"how to cook {dish_name} recipe tutorial",
            type="video"
        )
        response = request.execute()
        
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"YouTube API Error (likely quota exceeded): {e}")
        # Fallback link if API fails
        return f"https://www.youtube.com/results?search_query={dish_name.replace(' ', '+')}+recipe"
    
    return None