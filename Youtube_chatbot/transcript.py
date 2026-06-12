import requests
import streamlit as st
import os

class Transcript:
    @staticmethod
    def get_transcript(video_id: str):
        try:
            # Read token from Streamlit Cloud secrets or local .env fallback
            api_key = st.secrets.get("SCRAPER_API_KEY") or os.getenv("SCRAPER_API_KEY")
            
            if not api_key:
                print("Missing SCRAPER_API_KEY secret token configurations.")
                return None
                
            # 🟢 FIX: Remove the trailing forward slash from the end of the endpoint URL string!
            url = "https://api.scrapingdog.com/youtube/transcripts"
            
            params = {
                "api_key": api_key,
                "v": video_id
            }
            
            # Fire proxy-wrapped GET request
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if payload returned empty or invalid
                if not data:
                    print("API response payload is completely empty.")
                    return None
                
                # Unpack the transcripts dictionary wrapper array
                if "transcripts" in data and isinstance(data["transcripts"], list):
                    full_text = " ".join([segment["text"] for segment in data["transcripts"]])
                    return full_text
                else:
                    print(f"Unexpected response payload schema format from engine: {data}")
                    return None
                
            else:
                print(f"Scraper returned non-200 status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Bypass Scraper Engine Failed: {e}")
            return None