import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()


def generate_dataset():
    prompt = """
Generate a dataset of realistic customer support complaints for an e-commerce company.
Return a JSON array of 10 objects. Each object should have:
- "complaint": the customer's message (1-3 sentences, realistic and specific)
- "category": one of: "late_delivery", "wrong_item", "refund_request", "damaged_item", "account_issue"

Make the complaints feel real — include emotion, specific details, urgency levels.
Mix calm and angry customers. Mix simple and complex issues.

Respond with only the JSON array, no other text.
"""

    message = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1500,
    messages=[
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "["}  
    ]
)

    raw = "[" + message.content[0].text
    return json.loads(raw)


if __name__ == "__main__":
    dataset = generate_dataset()
    with open("dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Generated {len(dataset)} test cases")
    print(json.dumps(dataset[:2], indent=2))