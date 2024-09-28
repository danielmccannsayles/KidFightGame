import openai
from secret import OPENAI_KEY

# Set your OpenAI API key
openai.api_key = OPENAI_KEY

def generate_character_stats(description):
    # Define your system and user prompts
    system_prompt = (
        "You are a character creation assistant. "
        "When given a character description, you generate a JSON object with the character's stats."
    )

    user_prompt = f"Create a character with the following description: {description}."

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or use "gpt-3.5-turbo" if that's your subscription plan
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=50
    )

    # Extract and parse the structured JSON output
    reply = response['choices'][0]['message']['content']

    try:
        character_stats = eval(reply)  # Evaluate the JSON-like string safely
    except SyntaxError:
        print("Error parsing the output. The response was not a valid JSON.")
        character_stats = {}

    return character_stats

# Example usage
description = "A brave knight with unparalleled sword skills and a strong sense of justice."
character_stats = generate_character_stats(description)

print(character_stats)
