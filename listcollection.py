import chromadb

# Initialize Chroma DB client
client = chromadb.HttpClient(host='localhost', port=8000)#chromadb.Client()

# List all collections
# collections = client.list_collections()
# print("Existing collections:")
# for collection in collections:
#     print(collection.name)

print(client.get_collection("alto_k10_manual"))
