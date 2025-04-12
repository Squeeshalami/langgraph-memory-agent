import os
import uuid
import chromadb
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_ollama import OllamaEmbeddings
from utils import console, log_memory_search

# --- ChromaDB Setup ---#
# Initialize the embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")
# Directory to persist ChromaDB data
CHROMA_PATH = "agent_memories"
# Collection name within ChromaDB
COLLECTION_NAME = "agent_memories"

# Ensure the directory exists
os.makedirs(CHROMA_PATH, exist_ok=True)

# Initialize ChromaDB persistent client
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Initialize the Chroma vector store
store = Chroma(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
)

#--- Tools ---#
@tool
def save_memory(input_text: str) -> str:
    """
    Save specific facts, preferences, or details about the user to your memory for later recall.
    Use this proactively when the user shares information like:
    - Personal facts (e.g., "I've played drums for 17 years", "I live in London")
    - Preferences (e.g., "My favorite food is Mexican", "I like progressive metal music")
    - Key details mentioned in conversation that might be useful later.
    Do not save casual chat or information that isn't a specific fact or preference about the user.
    Do not save information that was just retrieved from memory - only save new information.
    The input should be the specific piece of information to save.
    """
    try:
        memory_content = input_text.strip()

        # Ensure there's actual content to save
        if not memory_content:
            return "Cannot save empty memory."

        # Check if this memory already exists to avoid duplicates
        existing_matches = store.similarity_search_with_score(memory_content, k=1)
        log_memory_search("Duplicate check for: " + memory_content, existing_matches)
        
        # If very similar content already exists (score below threshold), don't save
        if existing_matches and existing_matches[0][1] < 0.15:  # Lower score means higher similarity
            console.print(f"[bold blue]Memory Tool skipped saving:[/bold blue] '{memory_content}' (duplicate)")
            return f"Memory already exists, skipped saving duplicate: '{memory_content}'"

        memory_id = str(uuid.uuid4())

        store.add_texts(
            texts=[memory_content],
            ids=[memory_id],
            metadatas=[{"source": "user_memory"}],
        )
        # Print confirmation to the console
        console.print(f"[bold blue]Memory Tool saved:[/bold blue] '{memory_content}'")
        return f"Memory saved successfully: '{memory_content}'" # Return a confirmation string
    except Exception as e:
        console.print(f"[bold red]Error saving memory:[/bold red] {e}")
        return "Failed to save memory due to an error."
    

@tool
def search_memory(query: str) -> str:
    """
    Search your memory for specific information the user has previously told you.
    Only use this tool if the user explicitly asks you to remember something (e.g., "Do you remember...", "What did I tell you about...")
    or if answering their current query absolutely requires recalling past conversation details.
    Do not use this for general conversation or if the answer doesn't depend on past interactions.
    """
    try:
        # Perform the similarity search with scores
        results_with_scores = store.similarity_search_with_score(query, k=1) # change k value to adjust the number of results returned in the search

        log_memory_search(query, results_with_scores)

        # Check if any results were found before proceeding
        if not results_with_scores:
            return "I searched my memory, but couldn't find anything relevant to that."

        # Format the results for the agent (extract only the page_content)
        formatted_results = "\n".join([f"- {doc.page_content}" for doc, score in results_with_scores])
        return f"Okay, I checked my memory for '{query}'. Here's what I found:\n{formatted_results}"
    except Exception as e:
        console.print(f"[bold red]Error searching memory:[/bold red] {e}")
        return f"Sorry, I had trouble searching my memory. There was an error."
