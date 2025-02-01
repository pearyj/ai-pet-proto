import openai
import streamlit as st
from pet_logic import get_pet_response, parse_pet_response

# Make the page layout wide
st.set_page_config(layout="wide")


def main():
    st.title("AI Robot Pet Prototype (Streamlit)")

    st.markdown("""
    This interface lets you prototype an AI robot pet's reactions.  
    **1.** Enter some extra configuration or prompt instructions.  
    **2.** Describe your interaction with the pet.  
    **3.** See how the pet responds with eyes, movement, and sound.
    """)

    # Initialize or retrieve the pet's emotion from session state
    if "pet_emotion" not in st.session_state:
        st.session_state.pet_emotion = "Quite Happy"  # or any default

    # Initialize a "history" list if not present
    if "history" not in st.session_state:
        st.session_state.history = []

    # Let the user input their API key (masked):
    user_api_key = st.text_input("OpenAI API Key", type="password")

    # User input fields
    user_prompt_config = st.text_area(
        label="Pet Configuration / Prompt Engineering",
        value="",
        height=100,
        help="Enter extra instructions or personality tweaks for the pet."
    )

    user_interaction = st.text_area(
        label="User Interaction",
        value="I poke the pet and say hello.",
        height=100,
        help="Describe what you do or say to the pet."
    )

    configuration_prompt = user_prompt_config

    # Show + allow user to change the pet's current emotion.
    st.write("**Previously, the pet is feeling**:", st.session_state.pet_emotion)
    new_emotion = st.text_input("Change Pet Emotion (optional); please be descriptive:",
                                value=st.session_state.pet_emotion)

    # When the user clicks "Submit", call the OpenAI API
    if st.button("Submit"):
        if not user_api_key:
            st.error ("Please enter your API key first.")
        else:
            st.session_state.pet_emotion = new_emotion
            pet_response = get_pet_response(
                user_api_key,
                st.session_state.pet_emotion,
                configuration_prompt,
                user_interaction)
            st.subheader("Pet's Response")
            st.write(pet_response)

            # Parse the output for Eyes, Movement, Sound
            eyes_val, move_val, sound_val = parse_pet_response(pet_response)

            # Add a record to the "history" list
            st.session_state.history.append({
                "Prompt Config": user_prompt_config,
                "Emotion": new_emotion,
                "User Interaction": user_interaction,
                "Eyes": eyes_val,
                "Movement": move_val,
                "Sound": sound_val
            })

    if st.session_state.history:
        st.markdown("## Interaction History")
        st.dataframe(st.session_state.history, use_container_width=True)

if __name__ == "__main__":
    main()
