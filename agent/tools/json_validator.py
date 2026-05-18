import json


def validate_json_output(output: str) -> bool:
    try:
        json.loads(output)
        return True

    except json.JSONDecodeError:
        return False