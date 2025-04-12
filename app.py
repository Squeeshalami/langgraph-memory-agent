from graph import graph
from langchain_core.messages import HumanMessage
from utils import console


def main():
    # Initialize the thread id, this is used to identify the the conversation
    threadId = "1"
    config = {"configurable": {"thread_id": threadId}}

    # Welcome message
    console.print(f"[bold cyan]Welcome![/bold cyan] Type '[bold cyan]exit[/bold cyan]','[bold cyan]quit[/bold cyan]', or '[bold cyan]bye[/bold cyan]' to terminate the conversation.")
    console.print(f"[bold yellow]Assistant[/bold yellow]: Hello! How can I help you today?")

    # Main loop for the chat interface
    while True:
        try:
            user_input = console.input("[bold cyan]User[/bold cyan]>> ")
            if user_input.lower() in ["exit", "quit", "bye", "terminate",
                                      "/exit", "/quit", "/bye", "/terminate"]:
                
                console.print(f"[bold yellow]Assistant[/bold yellow]: Goodbye!")
                break

            if user_input.lower() == "":
                continue

            else:
                input_data = {"messages": [HumanMessage(content=user_input)]}

                # Invoke the main app
                result = graph.invoke(input_data, config=config)

                # Access the result messages from the final state
                if result and "messages" in result and result["messages"]:
                    # Check if the last message content is not None before printing
                    last_message_content = result['messages'][-1].content
                    if last_message_content is not None:
                         console.print(f"[bold yellow]Assistant[/bold yellow]: {last_message_content}")
                    else:
                         # Handle cases where the content might be None (e.g., tool call only)
                         console.print(f"[bold yellow]Assistant[/bold yellow]: (Action performed, no text response)")
                else:
                    console.print(f"[bold yellow]Assistant[/bold yellow]: (No message received)") # Handle cases where the result might be empty or malformed
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Assistant[/bold yellow]: Interrupted by user. Goodbye!")
            break

if __name__ == "__main__":
    main()
