import openai

openai.api_key = "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"

def generate_embeddings(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",  # Replace with your embedding model
        input=text
    )
    return response['data'][0]['embedding']

# Generate embeddings for the text content
embeddings = generate_embeddings("text_content")
