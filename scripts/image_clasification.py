from fastembed import ImageEmbedding
from qdrant_client import QdrantClient

# Initialize the Qdrant client
qdrant_client = QdrantClient("http://localhost:6333")

# Initialize the ImageEmbedding model
embedding = ImageEmbedding(model_name="Qdrant/clip-ViT-B-32-vision")

def classify_new_image(image_path):
    # Embed the new image
    new_image_embedding = list(embedding.embed([image_path]))[0]  # Convert generator to list and access the first item

    # Search for the closest match in the Qdrant collection
    collection_name = "image_classification"
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=new_image_embedding,
        limit=1  # We only need the closest result
    )

    # Extract the closest result
    if search_result:
        closest_result = search_result[0]
        closest_id = closest_result.id
        closest_label = closest_result.payload.get("label", "unknown")

        return closest_label
    else:
        return "unknown"