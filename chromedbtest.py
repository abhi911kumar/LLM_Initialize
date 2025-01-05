import chromadb

# Initialize Chroma client
client = chromadb.HttpClient(host='localhost', port=8000)

# Create a collection (similar to a table in a database)
client.delete_collection(name="example_collection")
collection = client.create_collection(name="example_collection")

# Add embeddings to the collection
collection.add(
    ids=["item1", "item2"],  # Unique identifiers for your items
    embeddings=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],  # Vector data
    metadatas=[{"name": "item1"}, {"name": "item2"}]  # Metadata for items
)

# Perform a similarity search
results = collection.query(
    query_embeddings=[[0.1, 0.2, 0.3]],  # The query vector
    n_results=1  # Number of similar results to retrieve
)

print(results)

