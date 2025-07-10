# Final updated code with corrections and improvements

import os
import dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Load environment
dotenv.load_dotenv()

# Initialize model
llm = init_chat_model("google_genai:gemini-2.0-flash")
print("LLM loaded...")
print(llm.invoke("Hey Chatgpt"))

# Neural search setup
class NeuralSearcher:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        self.qdrant_client = QdrantClient("http://localhost:6333")
        print("connected to Qdrant")

    def search(self, text: str):
        vector = self.model.encode(text).tolist()
        search_result = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=None,
            limit=20,
            with_payload=True,
            with_vectors=False
        ).points

        results = []
        min_keep = 5
        drop_threshold = 0.15
        last_score = None

        for i, hit in enumerate(search_result):
            score = hit.score
            payload = hit.payload
            results.append(payload['text'])
            if last_score is not None and i >= min_keep:
                if last_score - score >= drop_threshold:
                    break
            last_score = score

        return results

neural_searcher = NeuralSearcher(collection_name="case_preperation")

# State definition
class State(TypedDict):
    chat_hist: str
    user_query: str
    rag_query: str
    relevant_docs: list[dict]
    output: str
    intent: str

# Nodes
def check_intent(state: State):
    history_block = state['chat_hist']
    state['intent'] = llm.invoke(f"""
    System: You are an expert case interview assistant.
    Your task is to classify the user's intent based on their latest message and the conversation so far.
    Review the chat history and the current user message, then select the most appropriate intent label from the list below.
    Only output the label, with no explanation or extra text.

    Chat History:
    {history_block}

    User Message:
    {state['user_query']}

    Possible intent labels:
    - GENERATE_CASE: The user wants you to generate a new case interview question.
    - ANSWER_CASE: The user wants you to answer a specific case interview question.
    - ASK_FRAMEWORK: The user is asking about frameworks or approaches for solving cases.
    - HELP: The user is asking for help or guidance on how to use the assistant.
    - GENERAL_QUERY: The user is asking a general question not specific to cases or frameworks.
    - FEEDBACK: The user is asking feedback about their case interview performance or response.

    Output only the label from the list above.
    """).content.strip()
    return state


def get_rag_query(state: State) -> State:
    state["rag_query"] = llm.invoke(f"""
    Based on:
    User: {state['user_query']}
    Context: {state['chat_hist']}
    Intent: {state['intent']}
    Generate a search query for case prep docs.
    """).content
    return state

def fetch_docs(state: State) -> list[dict]:
    state["relevant_docs"] = neural_searcher.search(state["rag_query"])
    return state

def get_response(state: State) -> str:
    state["output"] = llm.invoke(f"""You are a case interview preparation assistant.
    This is some previous context of the state of your conversation: {state['chat_hist']},
    The user has asked the following question: {state['user_query']}
    The relevant documents that were retrieved from the RAG system are: {state['relevant_docs']}
    Generate a concise and informative response to the user's question based on the provided documents.
    Format clearly: concise paragraphs or bullet points when helpful.
    give feedbacks wherever necessary.
    """).content
    return state    

def store_history(state: State) -> State:
    state["chat_hist"]=llm.invoke(f"""You are an expert in summarizing multi-turn conversations for memory retention in a chatbot system.
        Here is the previous conversation context:
        {state['chat_hist']}
        The user has now asked this follow-up question:
        {state['user_query']}
        And the assistant responded with:
        {state['output']}
        Your task is to:
        - Generate a clear and concise summary of the entire conversation so far.
        - Include key details, decisions, and clarifications that could be important for future interactions.
        - Preserve any technical terms, frameworks, or examples discussed.
        - preserve the latest user query and assistant response.
        The summary should be in natural language and ready to be passed as context to an LLM in the next turn
            """).content.strip()
    print(state["chat_hist"])
    return state

workflow = StateGraph(State)
workflow.add_node("check_intent", check_intent)
workflow.add_node("get_rag_query", get_rag_query)
workflow.add_node("fetch_docs", fetch_docs)
workflow.add_node("get_response", get_response)
workflow.add_node("store_history", store_history)

workflow.add_edge(START, "check_intent")
workflow.add_edge("check_intent","get_rag_query")
workflow.add_edge("get_rag_query", "fetch_docs")
workflow.add_edge("fetch_docs", "get_response")
workflow.add_edge("get_response", "store_history")
workflow.add_edge("store_history", END)
chain = workflow.compile()

# # Main loop
# state = {
#     "chat_hist": "No previous conversation",
#     "user_query": "",
#     "rag_query": "",
#     "relevant_docs": [],
#     "output": "",
#     "intent": ""
# }

# while True:
#     user_query = input("Welcome to the case interview assistant! Enter your query (or 'exit'): ")
#     if user_query.lower() == "exit":
#         break
#     state["user_query"] = user_query
#     print("Processing...")
#     state = chain.invoke(state)
#     print("\nResponse:\n", state["output"])