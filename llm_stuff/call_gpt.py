import openai
import json
import pygame
from llm_stuff.secret import OPENAI_KEY
from llm_stuff.api_schema import API_SCHEMA
from llm_stuff.prompt import CHARACTER_PROMPT
from game_stuff.events import CHARACTER_RESPONSE_EVENT
from testing.mock_responses import TEST_CHARACTER_LIST

client = openai.OpenAI(api_key=OPENAI_KEY)

# Returns in the following JSON structure
"""
{
  "AD": 3,
  "HP": 4,
  "MS": 3,
  "Behavior": 2,
  "Strength": {
    "modifier": null,
    "against_id": null
  },
  "Weakness": {
    "modifier": 1,
    "against_id": 1
  },
  "Explanation": "The mobile pumpkin has modera.."
}"""


def generate_character_stats(
    description, color, post_event, character_list=TEST_CHARACTER_LIST
):
    """
    Generates character stats by calling GPT and then posts an event with the response.

    Args:
        description (str): Description of the character to generate.
        character_list (list): Current list of characters
        color (str): The color of the team ('white' or 'black')
        post_event (function): Callback to post the event back to the main thread.
    """
    info = f"""
    <Current Character List>
    {character_list}
    <End Current Character List>

    <Description>
    {description}
    <End Description>
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": CHARACTER_PROMPT},
                {"role": "user", "content": info},
            ],
            response_format={"type": "json_schema", "json_schema": API_SCHEMA},
        )
        reply = json.loads(response.choices[0].message.content)
        post_event(reply, color)
    except Exception as e:
        print(f"Error during API call: {e}")
        # TODO: consider handling error w/ event
