from dotenv import load_dotenv
from mistralai import Mistral
import os
import json


load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)


def analyze_security_findings(findings: list[dict]) -> str:
    prompt = f"""
    You are an AI Secure Coding Review Agent.

    Analyze the following deterministic scanner findings from a C#/.NET repository.

    Rules:
    - Only use the provided findings.
    - Do not invent files, line numbers, code snippets, or vulnerabilities.
    - If two findings refer to the same underlying issue, combine them into one result.
    - Return only a valid JSON array.
    - Do not wrap the JSON in markdown.
    - Do not include explanations before or after the JSON.
    - Use only these severity values: Low, Medium, High.

    Each result must contain:
    - vulnerability_type
    - file
    - lines
    - severity
    - explanation
    - recommendation

    Findings:
    {json.dumps(findings, indent=2)}
    """

    response = client.chat.complete(
        model="open-mistral-nemo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]  # type: ignore
    )

    return response.choices[0].message.content