import json
from statistics import mean


def generate_report():
    with open("results.json", "r") as f:
        results = json.load(f)

    persona_scores = {
        "professional": {"empathy": [], "accuracy": [], "resolution": []},
        "empathetic":   {"empathy": [], "accuracy": [], "resolution": []},
        "urgent":       {"empathy": [], "accuracy": [], "resolution": []}
    }

    for case in results:
        for persona_key, data in case["personas"].items():
            scores = data["scores"]
            persona_scores[persona_key]["empathy"].append(scores["empathy"])
            persona_scores[persona_key]["accuracy"].append(scores["accuracy"])
            persona_scores[persona_key]["resolution"].append(scores["resolution"])

    print("\n" + "="*55)
    print("       PERSONA EVALUATION REPORT")
    print("="*55)
    print(f"{'Persona':<16} {'Empathy':>9} {'Accuracy':>9} {'Resolution':>11} {'Overall':>9}")
    print("-"*55)

    overall_scores = {}

    for persona_key, dims in persona_scores.items():
        emp = mean(dims["empathy"])
        acc = mean(dims["accuracy"])
        res = mean(dims["resolution"])
        overall = mean([emp, acc, res])
        overall_scores[persona_key] = overall

        print(f"{persona_key.capitalize():<16} {emp:>9.1f} {acc:>9.1f} {res:>11.1f} {overall:>9.1f}")

    winner = max(overall_scores, key=overall_scores.get)
    print("="*55)
    print(f"\nBest overall persona: {winner.upper()}")
    print(f"Score: {overall_scores[winner]:.1f}/10")

    print("\nKey insight:")
    scores_list = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
    best, worst = scores_list[0], scores_list[-1]
    diff = best[1] - worst[1]
    print(f"  {best[0].capitalize()} outperformed {worst[0]} by {diff:.1f} points overall.")
    print("  This shows prompt persona design has measurable impact on response quality.")


if __name__ == "__main__":
    generate_report()