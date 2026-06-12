import requests
import streamlit as st
import os

class Transcript:
    @staticmethod
    def get_transcript(video_id: str):
        try:
            # 1. Dynamically read from Streamlit Cloud secrets OR local .env environment fallback
            api_key = st.secrets.get("SCRAPER_API_KEY") or os.getenv("SCRAPER_API_KEY")
            
            if not api_key:
                print("Missing SCRAPER_API_KEY secret token configurations.")
                return None
                
            url = "https://api.scrapingdog.com/youtube/transcripts/"
            
            params = {
                "api_key": api_key,
                "v": video_id
            }
            
            # 2. Fire high-speed proxy-wrapped GET request
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                # 3. Concatenate the segment text entries into a flat string paragraph
                full_text = " ".join([segment["text"] for segment in data])
                return full_text
                
            return None
        except Exception as e:
            print(f"Bypass Scraper Engine Failed: {e}")
            return None

# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

# api_client = YouTubeTranscriptApi()
# class Transcript:
#   @staticmethod
#   def get_transcript(video_id):
#     try:
#       transcript_list = api_client.fetch(video_id=video_id, languages=['en'])
#       transcript = " ".join(chunk.text for chunk in transcript_list)
#       return transcript
#     except TranscriptsDisabled:
#       print("No captions available for the video")
#     except Exception as e:
#       print(f"Unexpected error ocurred -: {e}")


# if __name__ == "__main__":
#   video_id = "c64hqovEG-U"
#   tr = Transcript()
#   caption = tr.get_transcript(video_id=video_id)
#   print(caption)

 