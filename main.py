import json
from anthropic import Anthropic
from dotenv import load_dotenv
from personas import PERSONAS
from grader import grade_response

load_dotenv()
client = Anthropic()


def generate_response(complaint, persona):
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        system=persona["system"],
        messages=[{"role": "user", "content": complaint}]
    )
    return message.content[0].text


def run_evaluation():
    with open("dataset.json", "r") as f:
        dataset = json.load(f)

    results = []

    for i, test_case in enumerate(dataset):
        complaint = test_case["complaint"]
        print(f"\nTest case {i+1}/{len(dataset)}: {test_case['category']}")

        case_result = {
            "complaint": complaint,
            "category": test_case["category"],
            "personas": {}
        }

        for persona_key, persona in PERSONAS.items():
            print(f"  Running {persona['name']} persona...")

            response = generate_response(complaint, persona)
            grades = grade_response(complaint, response, persona["name"])

            case_result["personas"][persona_key] = {
                "response": response,
                "scores": grades
            }

        results.append(case_result)

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nEvaluation complete. Results saved to results.json")
    return results


if __name__ == "__main__":
    run_evaluation()