from sentence_transformers import SentenceTransformer
import chromadb

# Initialize the Hugging Face embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize Chroma DB client
client = chromadb.HttpClient(host='localhost', port=8000) 

# Access the existing collection
collection_name = "alto_k10_manual"
collection = client.get_collection(name=collection_name)

while True:
    query_text = input("Enter your question (or 'quit' to exit): ")
    if query_text.lower() == "quit":
        break

    # Generate embedding for the query
    query_embedding = model.encode(query_text, convert_to_tensor=False)

    # Query the collection
    query_results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=3  # Retrieve top 3 most relevant chunks
    )

    # Display results
    if query_results["metadatas"]:
        print("Query Results:")
        for i, result in enumerate(query_results["metadatas"]):
            print(f"Result {i + 1}:")
            print(f"Content: {result[0]['content']}")
            # print(f"File Name: {result[0]['file_name']}") 
            print("-" * 40)
    else:
        print("No results found.")