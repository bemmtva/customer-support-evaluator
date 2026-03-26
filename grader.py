import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()


def grade_response(complaint, response, persona_name):
    grader_prompt = f"""
You are an expert customer support quality analyst.
Evaluate the following AI-generated support response to a customer complaint.

Customer complaint:
<complaint>
{complaint}
</complaint>

Support response (written in {persona_name} persona):
<response>
{response}
</response>

Score this response on exactly these three dimensions, each from 1 to 10:

1. empathy — Does the response acknowledge the customer's feelings appropriately for the persona?
2. accuracy — Is the response relevant and does it actually address the complaint?
3. resolution — Does the response provide a clear, actionable next step or solution?

Respond with only a JSON object in this exact format:
{{
    "empathy": <number 1-10>,
    "accuracy": <number 1-10>,
    "resolution": <number 1-10>,
    "reasoning": "<one sentence explaining the overall quality>"
}}
"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[
            {"role": "user", "content": grader_prompt},
            {"role": "assistant", "content": "{"}
        ]
    )

    raw = "{" + message.content[0].text
    return json.loads(raw)