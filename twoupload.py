from docx import Document
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize Chroma DB client
client = chromadb.HttpClient(host='localhost', port=8000)#chromadb.Client()

# Create or access the collection
collection_name = "alto_k10_manual"
client.delete_collection(name=collection_name)
collection = client.get_or_create_collection(name=collection_name)

# Extract and split text by titles and sections
def extract_sections_by_title(file_path):
    document = Document(file_path)
    sections = []
    current_title = None
    current_content = []
    
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text.isupper():  # Assuming titles are in uppercase
            if current_title:
                sections.append({"title": current_title, "content": "\n".join(current_content)})
            current_title = text
            current_content = []
        else:
            current_content.append(text)
    
    if current_title:
        sections.append({"title": current_title, "content": "\n".join(current_content)})
    
    return sections

# File path to the Word file
word_file_path = "./AltoK10_Owner's_Manual.docx"
sections = extract_sections_by_title(word_file_path)

# Initialize Hugging Face embedding model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


# Add sections to Chroma DB
for i, section in enumerate(sections):
    embedding = model.encode(section["content"], convert_to_tensor=False)
    collection.add(
        ids=[f"section_{i}"],
        embeddings=[embedding.tolist()],
        metadatas=[{"title": section["title"], "content": section["content"]}]
    )

print(f"Uploaded {len(sections)} sections to the collection '{collection_name}'.")
