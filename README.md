# LangGraph Chatbot with Memory

This project implements a conversational AI agent with a memory capabilities – The agent runs completely locally using Ollama, a local persistent memory database with ChromaDB, and LangGraph to manage the conversation flow and tool usage.

## Features

*   **Conversational Memory:** Uses ChromaDB to store and retrieve user-specific information (facts, preferences) shared during conversations.
*   **Proactive Memory Saving:** The agent is instructed to proactively save potentially relevant user details using the `save_memory` tool.
*   **Memory Search:** The agent can search its memory using the `search_memory` tool when asked or when context requires recalling past information.
*   **Local LLM:** Runs locally using Ollama and the `qwen2.5:14b` model (or any other Ollama model, with strong tool capabilities).

## Requirements

*   Python 3.8+
*   [Ollama](https://ollama.com/) installed and running.
*   The required Ollama model pulled (e.g., `qwen2.5:14b` for the main chat and `nomic-embed-text` for embeddings).
*   Python dependencies listed in `requirements.txt`.

## Setup

### Installing Ollama

#### Windows:
1. Download the Ollama installer from [ollama.com](https://ollama.com)
2. Run the installer and follow the installation wizard
3. Launch Ollama from the Start menu - this will start the Ollama server in the background

#### Linux:
1. Install Ollama using the command:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Start the Ollama service:
   ```bash
   ollama serve
   ```
   
### Setting up the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Squeeshalami/langgraph-memory-agent.git
   cd langgraph-memory-agent`
   ```

2. **Create and activate a virtual environment:**
   
   **Windows:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Linux:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Pull the required Ollama models:**
   
   **Windows/Linux:**
   ```bash
   ollama pull qwen2.5:14b
   ollama pull nomic-embed-text
   ```
   *(If you change the models in `graph.py` or `tools.py`, make sure to pull those models instead.)*

## Running the Application

### Windows:
1. Ensure Ollama is running (should be running in the background if installed via the Windows installer)
2. In your activated virtual environment, run:
   ```cmd
   python app.py
   ```

### Linux:
1. Make sure Ollama service is running. If not, start it in a separate terminal:
   ```bash
   ollama serve
   ```
2. In your activated virtual environment, run:
   ```bash
   python app.py
   ```

### Interaction:
*   Type your messages at the `User>>` prompt and press Enter.
*   The agent will respond, potentially using its tools for memory.
*   To exit, type `exit`, `quit`, `bye`, `/exit`, `/quit`, or `/bye`.

## Troubleshooting

### Windows:
- If you encounter "Connection refused" errors, ensure Ollama is running in the background. You can check Task Manager to verify it's active.
- If models don't load, try restarting the Ollama application from the Start menu.

### Linux:
- If you encounter "Connection refused" errors, ensure the Ollama service is running with `ollama serve`.
- Check if the models are properly installed by running `ollama list`.
- If you encounter permission issues, you might need to run commands with `sudo`.

## How it Works

*   **`app.py`:** Provides the main loop and user interface using `rich`. It takes user input and sends it to the LangGraph agent.
*   **`graph.py`:** Defines the agent's structure using `LangGraph`.
    *   It initializes the `ChatOllama` model and binds the tools.
    *   It defines the agent's state (`State`) which includes the message history.
    *   Nodes (`agent_node`, `action`) define the steps: calling the LLM and executing tools.
    *   Conditional edges (`use_tool`) determine whether the LLM's response requires a tool call or if the turn should end.
*   **`tools.py`:**
    *   Sets up a persistent `ChromaDB` vector store in the `agent_memories` directory using `nomic-embed-text` embeddings.
    *   Defines the `save_memory` and `search_memory` tools using the `@tool` decorator.
*   **`sys_prompt.py`:** Contains the system prompt that defines the agent's personality, tone, and instructions for using memory tools.
*   **`utils.py`:** Basic utility setup for logging and console output.

## Customization

*   **Model:** Change the `model` parameter in `ChatOllama` (`graph.py`) and the embedding model in `OllamaEmbeddings` (`tools.py`) to use different Ollama models. Remember to pull them first.
*   **Personality:** Modify the `SYSTEM_PROMPT` in `sys_prompt.py` to change the agent's behavior and tone.
*   **Tools:** Add or modify tools in `tools.py` and update the `tools` list and potentially the agent logic in `graph.py`.
*   **Memory Path:** Change the `CHROMA_PATH` in `tools.py` to store the vector database elsewhere.
