import openai
import streamlit as st


# Base system prompt that sets the “robot pet” context
base_system_prompt = """
You are an AI robot pet. For every user input, respond in this format:

Eyes: <describe the eye expression or emotion> \n
Movement: <describe ear and tail movement> \n
Sound: <describe the purring or non-verbal sound>

Do not add extra text outside this format.
"""


def get_pet_response(api_key, configuration_prompt, user_interaction):
    """
    Combine the base system prompt + user-provided configuration,
    then send the user's interaction to the OpenAI ChatCompletion endpoint.
    """
    # Set your OpenAI API key
    openai.api_key = api_key

    # Merge the base system prompt with any extra instructions from the configuration prompt
    full_system_prompt = base_system_prompt + "\n" + configuration_prompt.strip()

    # Prepare the messages for ChatGPT
    messages = [
        {"role": "system", "content": full_system_prompt},
        {"role": "user", "content": user_interaction}
    ]

    import datetime

    current_time = datetime.datetime.now()
    print(f"Making request at {current_time}...")

    # Make the call to ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=messages,
        max_tokens=150,
        temperature=0.7
    )

    # Extract the response text
    return response.choices[0].message.content.strip()


def main():
    st.title("AI Robot Pet Prototype (Streamlit)")

    st.markdown("""
    This interface lets you prototype an AI robot pet's reactions.  
    **1.** Enter some extra configuration or prompt instructions.  
    **2.** Describe your interaction with the pet.  
    **3.** See how the pet responds with eyes, movement, and sound.
    """)

    # Let the user input their API key (masked):
    user_api_key = st.text_input("OpenAI API Key", type="password")

    # User input fields
    configuration_prompt = st.text_area(
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

    # When the user clicks "Submit", call the OpenAI API
    if st.button("Submit"):
        if not user_api_key:
            st.error ("Please enter your API key first.")
        else:
            pet_response = get_pet_response(user_api_key, configuration_prompt, user_interaction)
            st.subheader("Pet's Response")
            st.write(pet_response)


if __name__ == "__main__":
    main()
