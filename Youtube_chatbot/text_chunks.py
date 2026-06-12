from langchain_text_splitters import RecursiveCharacterTextSplitter
from Youtube_chatbot.transcript import Transcript

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
class TextChunks:
    @staticmethod
    def create_chunks(text):
        try:
            chunks = splitter.create_documents([text])
            return chunks
        except Exception as e:
            print(f"Unexpected error ocurred -: {e}")
            return []

if __name__ == "__main__":
    video_id = "c64hqovEG-U"
    tr = Transcript()
    caption = tr.get_transcript(video_id=video_id)
    chunks = TextChunks.create_chunks(caption)
    print(len(chunks))