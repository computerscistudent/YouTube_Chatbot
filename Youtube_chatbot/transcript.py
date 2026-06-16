import requests
import streamlit as st
import os


class Transcript:

    @staticmethod
    def get_transcript(video_id: str):

        try:
            api_key = st.secrets.get("SCRAPER_API_KEY") or os.getenv("SCRAPER_API_KEY")

            if not api_key:
                print("❌ SCRAPER_API_KEY not found.")
                return None

            print(f"✅ API Key Loaded: {api_key[:6]}******")
            print(f"🎥 Video ID: {video_id}")

            url = "https://api.scrapingdog.com/youtube/transcripts"

            params = {
                "api_key": api_key,
                "video_id": video_id
            }

            response = requests.get(
                url=url,
                params=params,
                timeout=20
            )

            print("=" * 60)
            print("STATUS CODE:", response.status_code)
            print("RAW RESPONSE:")
            print(response.text)
            print("=" * 60)

            if response.status_code != 200:
                print(f"❌ API returned {response.status_code}")
                return None

            try:
                data = response.json()
            except Exception:
                print("❌ Response is not valid JSON")
                return None

            print("PARSED JSON:")
            print(data)

            if not data:
                print("❌ Empty JSON payload received")
                return None

            # Format 1
            if (
                isinstance(data, dict)
                and "transcripts" in data
                and isinstance(data["transcripts"], list)
            ):
                full_text = " ".join(
                    segment.get("text", "")
                    for segment in data["transcripts"]
                )

                print(f"✅ Transcript Length: {len(full_text)} chars")
                return full_text

            # Format 2
            if isinstance(data, list):

                full_text = " ".join(
                    segment.get("text", "")
                    for segment in data
                    if isinstance(segment, dict)
                )

                print(f"✅ Transcript Length: {len(full_text)} chars")
                return full_text

            print(f"❌ Unexpected Schema: {data}")
            return None

        except Exception as e:
            print(f"❌ Transcript Extraction Failed: {str(e)}")
            return None