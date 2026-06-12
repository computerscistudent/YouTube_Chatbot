
import streamlit as st
from Youtube_chatbot.transcript import Transcript
from Youtube_chatbot.text_chunks import TextChunks
from Youtube_chatbot.vector_store_and_retriever import VectorStoreRetriever
from Youtube_chatbot.augmentation import Augmentation
from langchain_core.messages import AIMessage, HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(page_title="YouTube RAG Chatbot", page_icon="🎥", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "setup"
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "chat_history" not in st.session_state:    
    st.session_state.chat_history = []
if "video_id" not in st.session_state:
    st.session_state.video_id = ""

def extract_video_id(url_or_id : str):
    """Helper to extract video ID if the user pastes a full YouTube URL"""
    if "v=" in url_or_id:
        return url_or_id.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url_or_id:
        return url_or_id.split("youtu.be/")[1].split("?")[0]
    return url_or_id.strip()

if st.session_state.page == "setup":
    st.title("🎥 YouTube RAG Chatbot Engine")
    st.write("Paste a YouTube video link below to ingest its transcript into a local vector storage matrix and start chatting with the video context!")
    st.markdown("----")

    user_input = st.text_input("Enter YouTube Video URL or Video ID:", placeholder="e.g., https://www.youtube.com/watch?v=c64hqovEG-U")
    if st.button("🚀 Initialize Chatbot Engine", use_container_width=True):
        if not user_input.strip():
            st.error("Please provide a valid YouTube URL or Video ID first.")
        else :
            with st.status("Building Knowledge Graph...", expanded=True) as status:
                try:
                    video_id = extract_video_id(user_input)
                    st.session_state.video_id = video_id
                    status.update(label="🔍 Checking local storage for pre-built vector cache...")
                    vector_store = VectorStoreRetriever.load_local_vectors(video_id=video_id)
                    if vector_store:
                        status.update(label="⚡ Cache found! Loading vectors instantly...")
                    else:
                        status.update(label="🔄 Step 1: Cache Missing. Fetching YouTube Transcript from API...")
                        caption = Transcript.get_transcript(video_id=video_id)
                        if not caption:
                            st.warning("⚠️ YouTube API rate-limited your IP. Falling back to locally cached transcript file...")
                            if os.path.exists("mock_transcript.txt"):
                                with open("mock_transcript.txt", "r", encoding="utf-8") as f:
                                    caption = f.read()
                            else:
                                raise Exception("Transcript Fetch Failed completely")
                        status.update(label="🧠 Step 2: Fragmenting Text Chunks...")
                        chunks = TextChunks.create_chunks(caption)

                        status.update(label="💾 Step 3: Generating OpenAI Embeddings & Compiling FAISS Matrix...")
                        vector_store = VectorStoreRetriever.create_and_store_vectors(chunks, video_id)

                    if not vector_store:
                        raise Exception("Vector Store compilation broken.")
                    
                    retriever = VectorStoreRetriever.build_retriever(vector_store=vector_store)
                    st.session_state.retriever = retriever

                    status.update(label="✅ Success! Pipeline Compiled.", state="complete")

                    st.session_state.page = "chat"
                    st.rerun()


                except Exception as e:
                    status.update(label="❌ Pipeline Failed", state="error")
                    st.error(f"Execution Error: {e}")


elif st.session_state.page == "chat":
    with st.sidebar:
        st.title("⚙️ Engine Stats")
        st.video(f"https://www.youtube.com/watch?v={st.session_state.video_id}")
        st.caption(f"Active Video ID: `{st.session_state.video_id}`")
        st.markdown("---")

        if st.button("🔄 Load a New Video", type="primary",use_container_width=True):
            st.session_state.page = "setup"
            st.session_state.retriever = None
            st.session_state.chat_history = []
            st.session_state.video_id = ""
            st.rerun()
    st.title("🤖 Chat Room: Discussing Video Context")
    st.write("The AI has stored the entire transcript memory structure. Ask it anything!")
    st.markdown("---")

    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)

    if user_query := st.chat_input("Ask anything about the video..."):
        with st.chat_message("user"):
            st.write(user_query)
        with st.spinner("Analyzing context snippets... 🤔"):
            if st.session_state.retriever is  None:
                st.error("No retriever available. Please load a video first.")
                st.rerun()
            retrieved_docs = st.session_state.retriever.invoke(user_query)
            context = "\n\n---\n\n".join(doc.page_content for doc in retrieved_docs)

            answer = Augmentation.augment_query(context=context, question=user_query, history=st.session_state.chat_history)

            with st.chat_message("assistant"):
                st.write(answer)

            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=answer))

            st.rerun()
