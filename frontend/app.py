import streamlit as st
import requests

# Title of the application
st.title("AI Receptionist for Dr. Adrin")

# Define the chatbot states
if 'state' not in st.session_state:
    st.session_state.state = 'initial'
    st.session_state.contact_method = None

# Initial state - ask user if they want to book an appointment or have an emergency
if st.session_state.state == 'initial':
    st.write("Welcome to Dr. Adrin's AI Receptionist.")
    option = st.radio(
        "Do you want to:",
        ("Book an appointment", "Report an emergency")
    )

    if st.button("Submit"):
        if option == "Report an emergency":
            st.session_state.state = 'emergency'
        else:
            st.write("Booking appointments is currently not supported. Please contact the clinic directly.")
            st.session_state.state = 'initial'  # Reset state
else:
    if st.session_state.state == 'emergency':
        st.write("Please enter the details of your emergency:")
        user_input = st.text_input("Emergency details:")

        if st.button("Send"):
            if not user_input:
                st.warning("Please enter your emergency details before sending.")
            else:
                try:
                    # Sending the emergency details to the backend API
                    response = requests.post(
                        'http://127.0.0.1:5000/chat',
                        json={'message': user_input}
                    )
                    
                    # Parse and display the JSON response
                    if response.status_code == 200:
                        response_data = response.json()
                        st.success(response_data.get('response', 'No response field in JSON'))
                        
                        # Ask the user for their preferred contact method
                        st.session_state.contact_method = st.selectbox(
                            "Please select your preferred contact method:",
                            ["Select", "Phone", "Email"]
                        )
                        
                        if st.session_state.contact_method == "Phone":
                            phone_number = st.text_input("Please enter your phone number:")
                            if st.button("Submit Phone Number"):
                                if not phone_number:
                                    st.warning("Please enter your phone number before submitting.")
                                else:
                                    st.success(f"Dr. Adrin will contact you via Phone at {phone_number} in a random time.")
                                    st.balloons()
                                    st.write("Thank you for reaching out!")
                                    st.session_state.state = 'initial'  # Reset state
                        elif st.session_state.contact_method == "Email":
                            email = st.text_input("Please enter your email address:")
                            if st.button("Submit Email"):
                                if not email:
                                    st.warning("Please enter your email address before submitting.")
                                else:
                                    st.success(f"Dr. Adrin will contact you via Email at {email} in a random time.")
                                    st.balloons()
                                    st.write("Thank you for reaching out!")
                                    st.session_state.state = 'initial'  # Reset state
                    else:
                        st.error(f"Error: Received status code {response.status_code}")
                        st.write("Raw response:", response.text)
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Request failed: {e}")
                except ValueError as e:
                    st.error(f"Failed to decode JSON response: {e}")
                    st.write("Raw response:", response.text)