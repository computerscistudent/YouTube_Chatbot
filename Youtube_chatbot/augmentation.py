from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from Youtube_chatbot.transcript import Transcript
from Youtube_chatbot.text_chunks import TextChunks
from Youtube_chatbot.vector_store_and_retriever import VectorStoreRetriever
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model= "gpt-4o-mini", temperature=0.7)

# prompt_template = PromptTemplate(
#     template="""
#             You are a helpful assistant that provides additional information to answer the user's question.
#             Use the following context to answer the question. If you don't know the answer, say you don't know.
#             Context: {context}
#             Question: {question}
#         """,
#         input_variables=["context", "question"]
# )

prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that analyzes a YouTube video transcript to answer a user's question.
        Use the provided context to answer the question. If you don't know the answer, say you don't know.

        Context:
        {context}"""),
        
        # This placeholder dynamically injects your list of Human and AI messages
        MessagesPlaceholder(variable_name="history"),
        
        ("human", "{question}")
    ])

class Augmentation:
    @staticmethod
    def augment_query(context, question, history):
        try:
            prompt = prompt_template.format_messages(
                context=context, 
                question=question, 
                history=history
            )
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Unexpected error ocurred -: {e}")
            return "Sorry, I couldn't process your request at the moment."

if __name__ == "__main__":
    video_id = "c64hqovEG-U"
    caption = Transcript().get_transcript(video_id=video_id)
    chunks = TextChunks.create_chunks(caption)
    vector_store = VectorStoreRetriever.create_and_store_vectors(chunks, video_id=video_id)
    if vector_store:
        print("Vector store got created successfully")
        retriever = VectorStoreRetriever.build_retriever(vector_store=vector_store)
        print("Retriever configured successfully!")
        if retriever:
            rez = retriever.invoke("Where are the sun's siblings")
            context = "\n\n---\n\n".join(doc.page_content for doc in rez)
            
            augmented_query = Augmentation.augment_query(context=context, question="What do you mean by the sun's siblings?", history=[])
            print(f"Augmented Query: {augmented_query}")