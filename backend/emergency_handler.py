import time
from qdrant_client import QdrantClient
from vectorization import vectorize_text

# Initialize Qdrant client
qdrant_client = QdrantClient(api_key='-Hp__kMlJSwNI3sn1E8DrcnSW2vobt_FKOgzjapn9rKxxf4MlKoQeQ')

def handle_emergency(emergency_text, user_location):
    """
    Handle the emergency reported by the user.
    
    Args:
        emergency_text (str): The description of the emergency provided by the user.
        user_location (str): The location of the user reporting the emergency.
        
    Returns:
        response (str): The appropriate next steps for the user to take.
        eta (str): Estimated time of arrival for the doctor.
    """
    
    # Inform the user that the system is processing their emergency
    interim_message = "I'm checking what you should do immediately. Meanwhile, can you tell me which area you're located in right now?"
    print(interim_message)  # In an actual chatbot, this would be sent to the user via chat.
    
    # Artificial delay to simulate processing time
    time.sleep(15)
    
    # Vectorize the emergency text using Google Gemini
    emergency_vector = vectorize_text(emergency_text)
    
    # Search in Qdrant for a similar emergency
    search_result = qdrant_client.search(
        collection_name='emergency_responses',
        query_vector=emergency_vector,
        limit=1
    )
    
    if search_result:
        # Extract the most relevant response from the database
        response = search_result[0].payload['response']
        
        # Estimated time of arrival for the doctor
        eta = f"Dr. Adrin will be arriving at your location in approximately {get_eta()} minutes."
        
        # Return the response and ETA
        return response, eta
    else:
        # If no match is found, provide basic first aid instructions
        response = "I couldn't find specific instructions for your emergency. Please follow basic first aid steps like ensuring the patient's airway is clear, stopping any bleeding, and keeping them comfortable."
        eta = f"Dr. Adrin will be arriving at your location in approximately {get_eta()} minutes."
        
        return response, eta

def get_eta():
    """
    Generate a random estimated time of arrival (ETA) for the doctor.
    
    Returns:
        eta (int): Randomly generated ETA in minutes.
    """
    import random
    return random.randint(5, 20)