from rich.console import Console

console = Console()


def log_memory_search(query: str, results_with_scores):
    console.print(f"[bold magenta]Memory Search Results for query:[/bold magenta] '{query}'")
    if results_with_scores:
        # Iterate through the list of (Document, score) tuples
        for i, (doc, score) in enumerate(results_with_scores):
            # Print the content and the score (formatted to 4 decimal places)
            # Note: Lower scores generally mean higher relevance in Chroma
            console.print(f"  [magenta]Result {i+1}:[/magenta] '{doc.page_content}' (Score: {score:.4f})")
    else:
        console.print("  [magenta]No results found.[/magenta]")
    
