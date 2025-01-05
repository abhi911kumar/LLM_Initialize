from docx import Document
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize Chroma DB client
client = chromadb.HttpClient(host='localhost', port=8000)#chromadb.Client()

# Create or access the collection
collection_name = "alto_k10_manual"
client.delete_collection(name=collection_name)
collection = client.create_collection(name=collection_name)

# Extract and split text from the Word file
file_path = "AltoK10_Owner's_Manual.docx"
def extract_and_split_text(file_path):
    document = Document(file_path)
    chunks = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:  # Only add non-empty paragraphs
            chunks.append(text)
    return chunks

text_chunks = extract_and_split_text(file_path)

# Initialize Hugging Face embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Upload each chunk as a separate entry
for i, chunk in enumerate(text_chunks):
    embedding = model.encode(chunk, convert_to_tensor=False)
    collection.add(
        ids=[f"chunk_{i}"],  # Unique ID for each chunk
        embeddings=[embedding.tolist()],
        metadatas=[{"file_name": file_path, "content": chunk}]
    )

print(f"Uploaded {len(text_chunks)} chunks to the collection '{collection_name}'.")
