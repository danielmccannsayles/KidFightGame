import openai
import json
from llm_stuff.secret import OPENAI_KEY
from llm_stuff.api_schema import API_SCHEMA
from llm_stuff.prompt import CHARACTER_PROMPT
from testing.mock_responses import TEST_CHARACTER_LIST, LARGE_SPIKED_BALL_RESPONSE

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
