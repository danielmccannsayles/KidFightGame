import openai
import json
import pygame
from llm_stuff.secret import OPENAI_KEY
from llm_stuff.api_schema import API_SCHEMA
from llm_stuff.prompt import CHARACTER_PROMPT
from game_stuff.events import CHARACTER_RESPONSE_EVENT
from testing.mock_responses import TEST_CHARACTER_LIST

client = openai.AsyncOpenAI(api_key=OPENAI_KEY)

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


async def agenerate_character_stats(description: str, character_list: list):
    # Prompts
    info = f"""
<Current Character List>
{character_list}
<End Current Character List>

<Description>
{description}
<End Description>
    """

    # Call API
    print("calling api")
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": CHARACTER_PROMPT},
            {"role": "user", "content": info},
        ],
        response_format={"type": "json_schema", "json_schema": API_SCHEMA},
    )
    print("response returned")
    reply = json.loads(response.choices[0].message.content)
    return reply


async def acreate_character(
    description, color, character_list: list = TEST_CHARACTER_LIST
):
    print("acreate_character - calling generate")
    response = await agenerate_character_stats(description, character_list)
    print("acreate_charfacter - posting event")
    pygame.event.post(
        pygame.event.Event(
            CHARACTER_RESPONSE_EVENT, {"response": response, "color": color}
        )
    )
