# vectorization.py

import spacy

# Load a pre-trained spaCy model
nlp = spacy.load('en_core_web_sm')  # or another model of your choice

def vectorize_text(text):
    """
    Convert the input text to a vector representation using spaCy.
    
    Args:
        text (str): The text to be vectorized.
    
    Returns:
        vector (np.ndarray): The vector representation of the text.
    """
    doc = nlp(text)
    return doc.vector