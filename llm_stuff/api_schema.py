API_SCHEMA = {
    "name": "character_stats",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "HP": {"type": "integer"},
            "AD": {"type": "integer"},
            "MS": {"type": "integer"},
            "Behavior": {"type": "integer"},
            "Strength": {
                "type": "object",
                "properties": {
                    "against_id": {"type": ["integer", "null"]},
                    "modifier": {"type": ["integer", "null"]},
                },
                "required": ["against_id", "modifier"],
                "additionalProperties": False,
            },
            "Weakness": {
                "type": "object",
                "properties": {
                    "against_id": {"type": ["integer", "null"]},
                    "modifier": {"type": ["integer", "null"]},
                },
                "required": ["against_id", "modifier"],
                "additionalProperties": False,
            },
            "Explanation": {"type": "string"},
        },
        "required": [
            "HP",
            "AD",
            "MS",
            "Behavior",
            "Strength",
            "Weakness",
            "Explanation",
        ],
        "additionalProperties": False,
    },
}
