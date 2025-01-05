from docx import Document

def extract_content_with_grid(file_path):
    """
    Extracts both text content and grid data (tables) from a Word document.
    """
    document = Document(file_path)
    chunks = []

    for element in document.element.body:
        if element.tag.endswith("p"):  # Paragraphs
            text = element.text.strip()
            if text:  # Non-empty paragraphs
                chunks.append({"type": "text", "content": text})
        elif element.tag.endswith("tbl"):  # Tables (Grid Data)
            table_data = []
            for row in element.findall(".//w:tr", namespaces=element.nsmap):
                row_data = [
                    cell.text.strip() if cell.text else ""
                    for cell in row.findall(".//w:tc", namespaces=element.nsmap)
                ]
                table_data.append(row_data)
            if table_data:  # Non-empty tables
                chunks.append({"type": "table", "content": table_data})

    return chunks

# Example usage
file_path = "./AltoK10_Owner's_Manual.docx"
document_chunks = extract_content_with_grid(file_path)

# Debugging: Print extracted chunks
for chunk in document_chunks:
    print(f"Type: {chunk['type']}")
    if chunk['type'] == "text":
        print(chunk["content"])
    elif chunk['type'] == "table":
        for row in chunk["content"]:
            print(row)
    print("-" * 40)
