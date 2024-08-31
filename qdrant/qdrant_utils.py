from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import numpy as np

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url="e4561ed8-431b-46ce-aedc-400df1814311.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    api_key="-Hp__kMlJSwNI3sn1E8DrcnSW2vobt_FKOgzjapn9rKxxf4MlKoQeQ",
)

# Define the collection name
collection_name = "emergency_responses"

# Delete the collection if it already exists (to recreate with correct dimensions)
if qdrant_client.collection_exists(collection_name):
    qdrant_client.delete_collection(collection_name)

# Create the collection with the correct vector dimension
qdrant_client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(size=96, distance=models.Distance.COSINE),
)

# Define the emergency data
emergencies = [
    {"emergency_type": "had heart attack", "response": "Start CPR immediately. Push against the chest of the patient and blow air into their mouth in a constant rhythm."},
    {"emergency_type": "severe bleeding", "response": "Apply direct pressure to the wound. Keep the patient calm and seek immediate medical attention."},
    {"emergency_type": "choking", "response": "Perform the Heimlich maneuver. If the person cannot breathe, call emergency services immediately."},
    {"emergency_type": "burns", "response": "Cool the burn under running water for at least 10 minutes. Cover with a clean, non-stick dressing and seek medical attention."},
    {"emergency_type": "fracture", "response": "Immobilize the fractured area and avoid moving it. Apply ice to reduce swelling and seek medical attention."},
    {"emergency_type": "stroke", "response": "Seek immediate medical attention. Symptoms may include sudden numbness, confusion, or difficulty speaking or walking."},
    {"emergency_type": "allergic reaction", "response": "Administer an antihistamine if appropriate and seek medical help if symptoms are severe, such as difficulty breathing or swelling."},
    {"emergency_type": "heatstroke", "response": "Move to a cooler environment, hydrate with water, and seek medical attention if symptoms are severe like confusion or unconsciousness."},
    # Add more emergencies as needed
]

# Function to vectorize text (improved implementation)
def vectorize_text(text):
    # Placeholder for vectorization logic
    # For a real-world scenario, use a pre-trained model like BERT, FastText, etc.
    # Here, we use random vectors for demonstration purposes
    vector = np.random.rand(96).tolist()
    return vector

# Insert the emergency data into the collection
for emergency in emergencies:
    point_id = str(uuid.uuid4())  # Generate a UUID for the point ID
    vector = vectorize_text(emergency["emergency_type"])  # Vectorize the emergency type
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=point_id,
                vector=vector,  # Use the correct dimension vector
                payload=emergency
            )
        ]
    )

print("Emergency responses collection created and data inserted successfully.")