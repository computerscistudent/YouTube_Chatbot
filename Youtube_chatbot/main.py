import sys
from Youtube_chatbot.transcript import Transcript
from Youtube_chatbot.text_chunks import TextChunks
from Youtube_chatbot.vector_store_and_retriever import VectorStoreRetriever
from Youtube_chatbot.augmentation import Augmentation
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from typing import List

def extract_video_id(url_or_id : str):
    """Helper to extract video ID if the user pastes a full YouTube URL"""
    if "v=" in url_or_id:
        return url_or_id.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url_or_id:
        return url_or_id.split("youtu.be/")[1].split("?")[0]
    return url_or_id.strip()

chat : List[BaseMessage] = [] 

def run_chatbot():
    print("="*60)
    print("🎥 WELCOME TO THE YOUTUBE RAG CHATBOT CLI 🎥")
    print("="*60)

    user_input = input("Enter YouTube Video URL or Video ID: ")
    video_id = extract_video_id(user_input)

    print("\n🔄 Fetching video transcript...")
    caption = Transcript.get_transcript(video_id=video_id)
    if not caption:
        print("❌ Could not load transcript. Exiting.")
        return
    
    print("🧠 Chunking text and generating embeddings...")
    chunks = TextChunks.create_chunks(caption)
    vector_store = VectorStoreRetriever.create_and_store_vectors(chunks,video_id)
    if not vector_store:
        print("❌ Failed to initialize Vector Database. Exiting.")
        return
    
    retriever = VectorStoreRetriever.build_retriever(vector_store=vector_store)
    if not retriever:
        print("❌ Failed to initialize Retriever. Exiting.")
        return
    print("✅ Chatbot Engine Initialized Successfully!")
    print("="*60)
    print("🤖 Ask anything about the video! (Type 'exit' to quit)")
    print("="*60)

    while True:
        question = input("\n👤 You: ")
        if question.lower() in ['exit', 'quit', 'q']:
            print("\n🤖 Bot: Goodbye, brother! Have a great day!")
            break

        if not question.strip():
            continue
            
        print("Thinking... 🤔")

        retrieved_docs = retriever.invoke(question)
        context = "\n\n---\n\n".join(doc.page_content for doc in retrieved_docs)

        answer = Augmentation.augment_query(context=context, question=question, history=chat)
        chat.append(HumanMessage(content=question))
        chat.append(AIMessage(content=answer))
        print(f"\n🤖 Bot: {answer}")
        print("-" * 40)
    
    

if __name__ == "__main__":
    run_chatbot()
    print(f"\n📜 Conversation History: {chat}" )


# What do you mean by the sun's siblings
# explain about life on exomoons 
# explain the previous question but in easier words