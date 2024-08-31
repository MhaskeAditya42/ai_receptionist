from flask import Flask, request, jsonify
import time
from qdrant_client import QdrantClient
from qdrant_client.http import models
from vectorization import vectorize_text

app = Flask(__name__)

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url="e4561ed8-431b-46ce-aedc-400df1814311.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="-Hp__kMlJSwNI3sn1E8DrcnSW2vobt_FKOgzjapn9rKxxf4MlKoQeQ",
)

# Ensure the collection exists
collection_name = "emergency_responses"
if not qdrant_client.collection_exists(collection_name):
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=96, distance=models.Distance.COSINE),  # Ensure vector size matches the actual vectorization
    )

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').lower()

        if "emergency" in message:
            response = handle_emergency(message)
        else:
            response = "Thanks for the message, we will forward it to Dr. Adrin."

        return jsonify({"response": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handle_emergency(emergency_text):
    time.sleep(5)  # Artificial delay

    # Vectorize the emergency text
    emergency_vector = vectorize_text(emergency_text)

    # Search in Qdrant
    search_result = qdrant_client.search(
        collection_name=collection_name,
        query_vector=emergency_vector,
        limit=1
    )

    if search_result:
        # Extract the response from the search result
        response = search_result[0].payload.get('response', 'No response available.')
        return f"{response} I'm checking what you should do immediately. Meanwhile, can you tell me which area you're located in right now? Dr. Adrin will arrive in approximately 10 minutes."
    else:
        return "I don't understand what you are saying. Please provide more details or describe the emergency in a different way."

if __name__ == '__main__':
    app.run(debug=True)