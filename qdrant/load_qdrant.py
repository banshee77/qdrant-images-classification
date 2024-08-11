from qdrant_client import QdrantClient, models
from fastembed import ImageEmbedding
from qdrant_client.models import PointStruct, VectorParams, Distance
import os
from PIL import Image

# Initialize the Qdrant client
client = QdrantClient("http://localhost:6333")

# Initialize lists to store image paths and labels
image_paths = []
labels = []

# Directories for human and not human images
root_dir = 'images_dataset'

# Collect image paths and labels
for label_dir in ['human', 'not_human']:
    label_path = os.path.join(root_dir, label_dir)
    for subdir, _, files in os.walk(label_path):
        for file in files:
            if file.lower().endswith(".jpg"):
                image_paths.append(os.path.join(subdir, file))
                labels.append(label_dir)
                
# Initialize the ImageEmbedding model
model = ImageEmbedding(model_name="Qdrant/clip-ViT-B-32-vision")

print(image_paths)

# Generate embeddings
embeddings = list(model.embed(image_paths))

# Create Qdrant collection
collection_name = "image_classification"
client.delete_collection(collection_name)
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE)
)

# Insert points into Qdrant
points = [
    PointStruct(id=idx, vector=embedding, payload={"path": image_paths[idx], "label": labels[idx]})
    for idx, embedding in enumerate(embeddings)
]
client.upsert(collection_name=collection_name, points=points)


print("--- Loading to qdrant completed ---")
