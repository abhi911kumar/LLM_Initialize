from docx import Document
from sentence_transformers import SentenceTransformer
import chromadb

# File path for the Word document
file_path = "./AltoK10_Owner's_Manual.docx"

# Function to extract text from Word document
def extract_text_from_word(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()

# Initialize the Hugging Face embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize Chroma DB client
client = chromadb.HttpClient(host='localhost', port=8000)#chromadb.Client()

# Create a collection
collection_name = "alto_k10_manual"
client.delete_collection(name=collection_name)
collection = client.create_collection(name=collection_name)

# Process the Word document
text_content = extract_text_from_word(file_path)

# Generate embeddings
embeddings = model.encode(text_content, convert_to_tensor=False)

# Add data to the Chroma DB collection
collection.add(
    ids=["alto_k10_doc"],
    embeddings=[embeddings.tolist()],  # Convert tensor to list if necessary
    metadatas=[{"file_name": file_path, "content": text_content}]
)

print(f"File '{file_path}' has been successfully uploaded to Chroma DB in the '{collection_name}' collection!")
