from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import chromadb

# Initialize Chroma DB HTTP client
client = chromadb.HttpClient(host='localhost', port=8000)

# Access the collection
collection_name = "alto_k10_manual"
collection = client.get_collection(name=collection_name)

# Initialize embedding model
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize T5 tokenizer and model
t5_tokenizer = AutoTokenizer.from_pretrained("t5-small")
t5_model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

# Function for summarization using T5
def t5_summarize(text, max_length=100, min_length=30):
    input_ids = t5_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = t5_model.generate(input_ids, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    return t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Function to query and summarize results
def query_and_summarize(query_text, n_results=3):
    # Generate embedding for the query
    query_embedding = embedding_model.encode(query_text, convert_to_tensor=False)
    
    # Query the collection
    query_results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )
    
    # Check if results are found
    if "metadatas" in query_results and len(query_results["metadatas"]) > 0:
        summaries = []
        for i, result_metadata in enumerate(query_results["metadatas"]):
            # Ensure content exists
            if len(result_metadata) > 0:
                content = result_metadata[0].get("content", "")
                if content:
                    # Generate summary for the retrieved chunk using T5
                    summary = t5_summarize(content, max_length=100, min_length=30)
                    summaries.append(f"Result {i + 1}: {summary}")
        
        if summaries:
            return "\n\n".join(summaries)
        else:
            return "No meaningful results found in the retrieved data."
    else:
        return "No relevant results found in the database."

# Interactive question-answering loop
def interactive_qa():
    print("Welcome to the Alto K10 Manual QA System!")
    print("Type your questions below, or type 'quit' to exit.\n")
    
    while True:
        # Prompt user for a query
        user_query = input("Your Question: ")
        
        # Exit condition
        if user_query.strip().lower() == "quit":
            print("Goodbye! Have a great day!")
            break
        
        # Get summarized results for the query
        print("\nProcessing your query...\n")
        try:
            summarized_results = query_and_summarize(user_query)
        except Exception as e:
            summarized_results = f"An error occurred while processing your query: {str(e)}"
        
        # Display the results
        print("Answer:")
        print(summarized_results)
        print("\n" + "=" * 40 + "\n")

# Run the interactive QA system
if __name__ == "__main__":
    interactive_qa()
