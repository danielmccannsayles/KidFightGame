import openai
import json
from .secret import OPENAI_KEY
from .api_schema import API_SCHEMA
from .prompt import CHARACTER_PROMPT

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

# TODO: get rid of this and generate the char list programatically
TEST_CHARACTER_LIST = [
    {"id": 0, "description": "rats with bombs attached"},
    {"id": 1, "description": "stone golem"},
]


# This is currently blocking btw. Can make it async in the future if needed
def generate_character_stats(
    description: str, character_list: list = TEST_CHARACTER_LIST
):
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
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": CHARACTER_PROMPT},
            {"role": "user", "content": info},
        ],
        response_format={"type": "json_schema", "json_schema": API_SCHEMA},
    )
    reply = json.loads(response.choices[0].message.content)
    return reply


description = "Five headed sea serpent"

# generate_character_stats(description)
