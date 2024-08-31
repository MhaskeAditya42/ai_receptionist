

# AI Receptionist for Dr. Adrin

## Overview

The AI Receptionist project is designed to handle emergency messages and general queries for Dr. Adrin. It uses Flask for the backend, Qdrant for vector search, and Streamlit for the frontend interface.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Backend Setup](#backend-setup)
- [Qdrant Setup](#qdrant-setup)
- [Frontend Setup](#frontend-setup)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.11 or higher
- Pip (Python package installer)
- Access to Qdrant Cloud instance
- Access to Google Gemini API (if applicable)

## Backend Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ai_receptionist.git
   cd ai_receptionist
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the necessary Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Qdrant Client**

   Create a `qdrant_utils.py` file inside the `qdrant` directory with the following content:

   ```python
   from qdrant_client import QdrantClient

   # Initialize the Qdrant client
   qdrant_client = QdrantClient(
       url="YOUR_QDRANT_URL",
       api_key="YOUR_QDRANT_API_KEY",
   )

   def create_emergency_collection():
       collection_name = 'emergency_messages'
       collection_config = {
           "vector_size": 300,  # Adjust based on your vector size
           "distance": "Cosine"  # or "Euclidean" based on your needs
       }

       qdrant_client.create_collection(
           collection_name=collection_name,
           config=collection_config
       )

   def add_emergency_messages():
       emergencies = [
           {"emergency_type": "not breathing", "response": "Start CPR immediately. Push against the chest of the patient and blow air into their mouth in a constant rhythm."},
           {"emergency_type": "severe bleeding", "response": "Apply direct pressure to the wound. Keep the patient calm and seek immediate medical attention."},
           # Add more emergencies as needed
       ]

       points = []
       for i, emergency in enumerate(emergencies):
           vector = vectorize_text(emergency["emergency_type"])
           points.append({
               "id": i,
               "vector": vector,
               "payload": {"response": emergency["response"]}
           })

       qdrant_client.upsert(
           collection_name='emergency_messages',
           points=points
       )

   def vectorize_text(text):
       # Replace with your vectorization logic
       return some_vectorize_function(text)
   ```

   Replace `YOUR_QDRANT_URL` and `YOUR_QDRANT_API_KEY` with your Qdrant Cloud URL and API key.

5. **Create Flask App**

   Create a `setup.py` file inside the `qdrant` directory with the following content:

   ```python
   from qdrant_utils import create_emergency_collection, add_emergency_messages

   if __name__ == "__main__":
       create_emergency_collection()
       add_emergency_messages()
   ```

   Run the script to set up the Qdrant collection and add emergency messages:

   ```bash
   python qdrant/setup.py
   ```

6. **Run Flask Backend**

   Create a `main.py` file in the root directory with the following content:

   ```python
   from flask import Flask, request, jsonify
   from qdrant_utils import qdrant_client, vectorize_text

   app = Flask(__name__)

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
       emergency_vector = vectorize_text(emergency_text)
       search_result = qdrant_client.search(
           collection_name='emergency_messages',
           query_vector=emergency_vector,
           limit=1
       )

       if search_result:
           response = search_result[0].payload['response']
           return f"I'm checking what you should do immediately. Meanwhile, can you tell me which area you're located in right now? Dr. Adrin will arrive in approximately 10 minutes."
       else:
           return "Please follow basic first aid."

   if __name__ == '__main__':
       app.run(debug=True)
   ```

   Start the Flask server:

   ```bash
   python main.py
   ```

## Frontend Setup

1. **Install Streamlit**

   ```bash
   pip install streamlit
   ```

2. **Create Streamlit App**

   Create a file named `app.py` in the `frontend` directory with the following content:

   ```python
   import streamlit as st
   import requests

   st.title("AI Receptionist for Dr. Adrin")

   user_input = st.text_input("Please enter your message or emergency:")

   if st.button("Send"):
       response = requests.post(
           'http://localhost:5000/chat',
           json={'message': user_input}
       ).json()

       st.write(response['response'])
   ```

3. **Run Streamlit App**

   ```bash
   streamlit run frontend/app.py
   ```

## Testing

1. **Test the Backend**

   Use Postman or a similar tool to send POST requests to `http://localhost:5000/chat` with the JSON payload:

   ```json
   {
       "message": "The patient is not breathing"
   }
   ```

   Ensure you receive the appropriate emergency response or message.

2. **Test the Frontend**

   Open the Streamlit app in your browser at `http://localhost:8501` and interact with the interface to ensure it communicates correctly with the Flask backend.

## Troubleshooting

- **Qdrant Errors**: Verify that your Qdrant URL and API key are correct. Ensure the Qdrant service is running and accessible.

- **Streamlit Errors**: If you encounter issues with Streamlit, ensure you have the correct version of `protobuf` and other dependencies installed.

- **Backend Errors**: Check the Flask logs for any errors and ensure that the Qdrant client is properly configured.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to adjust the content according to your specific setup and requirements.
