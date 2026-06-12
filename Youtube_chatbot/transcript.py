from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

api_client = YouTubeTranscriptApi()
class Transcript:
  @staticmethod
  def get_transcript(video_id):
    try:
      transcript_list = api_client.fetch(video_id=video_id, languages=['en'])
      transcript = " ".join(chunk.text for chunk in transcript_list)
      return transcript
    except TranscriptsDisabled:
      print("No captions available for the video")
    except Exception as e:
      print(f"Unexpected error ocurred -: {e}")


if __name__ == "__main__":
  video_id = "c64hqovEG-U"
  tr = Transcript()
  caption = tr.get_transcript(video_id=video_id)
  print(caption)

 