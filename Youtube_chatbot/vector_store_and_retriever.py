from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from Youtube_chatbot.text_chunks import TextChunks
from Youtube_chatbot.transcript import Transcript
import os
from dotenv import load_dotenv
load_dotenv()

embedding = OpenAIEmbeddings(model= "text-embedding-3-small")

class VectorStoreRetriever: 
    @staticmethod
    def create_and_store_vectors(documents:list[Document], video_id: str):
        try:
            vector_store = FAISS.from_documents(documents=documents,embedding=embedding)
            folder_name = f"faiss_{video_id}"
            vector_store.save_local(folder_path=folder_name)
            print(f"💾 Vector store saved locally to directory: '{folder_name}'")
            return vector_store
        except Exception as e:
            print(f"Unexpected error ocurred -: {e}")
            return None
    
    @staticmethod
    def load_local_vectors(video_id:str):
        """Loads a pre-existing vector store from disk instantly without calling OpenAI Embeddings"""
        try:
            folder_name = f"faiss_{video_id}"
            if os.path.exists(folder_name):
                vector_store = FAISS.load_local(
                    folder_name, 
                    embedding, 
                    allow_dangerous_deserialization=True
                )
                print(f"⚡ Instant Load! Retreived local cache index from directory: '{folder_name}'")
                return vector_store
            return None
        except Exception as e:
            print(f"Unexpected error occurred during load -: {e}")
            return None
    
    @staticmethod
    def build_retriever(vector_store):
        try:
            if vector_store:
                retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k':4})
                return retriever
        except Exception as e:
            print(f"Unexpected error ocurred -: {e}")
            return None
            

if __name__ == "__main__":
    video_id = "c64hqovEG-U"
    caption = Transcript().get_transcript(video_id=video_id)
    chunks = TextChunks.create_chunks(caption)
    vector_store = VectorStoreRetriever.create_and_store_vectors(chunks, video_id=video_id)
    if vector_store:
        print("Vector store got created successfully")
        #print(vector_store.index_to_docstore_id)

        retriever = VectorStoreRetriever.build_retriever(vector_store=vector_store)
        print("Retriever configured successfully!")

        if retriever:
            rez = retriever.invoke("Where are the sun's siblings")
            for i, doc in enumerate(rez):
                print(f"Document {i+1}: {doc.page_content}\n")
            context = "\n\n---\n\n".join(doc.page_content for doc in rez)
            #context = context.replace("\n", " ")
            print("\n\n")
            print(f"Context: {context}")
