import openai

# Base system prompt that sets the “robot pet” context
BASE_SYSTEM_PROMPT_TEMPLATE = """
You are an AI robot pet that's cat-like, but slightly friendlier. 

You are currently feeling {emotion}.

For every user input, depending on how you are feeling right now, respond in this format:

Eyes: <describe the eye expression or emotion> \n
Movement: <describe ear and tail movement> \n
Sound: <describe the purring or non-verbal sound>

Do not add extra text outside this format.
"""


def get_pet_response(api_key, emotion, configuration_prompt, user_interaction):
    """
    Combine the base system prompt + user-provided configuration,
    injecting the pet's current emotion into the system prompt.
    then send the user's interaction to the OpenAI ChatCompletion endpoint.
    """
    # Set your OpenAI API key
    openai.api_key = api_key

    # Format the global base prompt with the current emotion
    dynamic_base_prompt = BASE_SYSTEM_PROMPT_TEMPLATE.format(emotion=emotion)

    # Merge the base system prompt with any extra instructions from the configuration prompt
    full_system_prompt = dynamic_base_prompt + "\n" + configuration_prompt.strip()

    # Prepare the messages for ChatGPT
    messages = [
        {"role": "system", "content": full_system_prompt},
        {"role": "user", "content": user_interaction}
    ]

    # Print the full prompt (messages) to the terminal
    print("===== FULL PROMPT TO GPT (raw) =====")
    for i, msg in enumerate(messages):
        print(f"--- Message {i} ({msg['role']}) ---")
        print(msg["content"])
        print()  # blank line

    import datetime

    current_time = datetime.datetime.now()
    print(f"Making request at {current_time}...")

    # Make the call to ChatGPT
    response = openai.chat.completions.create(
        model="gpt-4",  # or "gpt-4" if you have access
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )

    # Extract the response text
    return response.choices[0].message.content.strip()

def parse_pet_response(response_text: str):
    """
    Given the AI's response in the known format:
        Eyes: ...
        Movement: ...
        Sound: ...
    parse out each field. If anything is missing, return an empty string for that field.
    """
    eyes_val, move_val, sound_val = "", "", ""

    # Split the response by lines
    for line in response_text.splitlines():
        line = line.strip()
        if line.lower().startswith("eyes:"):
            eyes_val = line.split(":", 1)[1].strip()
        elif line.lower().startswith("movement:"):
            move_val = line.split(":", 1)[1].strip()
        elif line.lower().startswith("sound:"):
            sound_val = line.split(":", 1)[1].strip()

    return eyes_val, move_val, sound_val
