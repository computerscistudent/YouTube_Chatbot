from Youtube_chatbot.transcript import Transcript

video_id = "c64hqovEG-U"
print("Testing your local Transcript utility module directly...")

try:
    caption = Transcript.get_transcript(video_id=video_id)
    print(f"\n--- DEBUG RESULT ---")
    print(f"Data type returned: {type(caption)}")
    if caption:
        print(f"Success! Character length: {len(caption)}")
        print(f"Content preview: {caption[:200]}...")
    else:
        print("Warning: The module returned an empty value (None or empty string)!")
except Exception as e:
    print(f"The module crashed with an exception: {e}")