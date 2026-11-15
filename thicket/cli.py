import argparse
from .core import SCENARIOS, explore_evaluate_decide


def main():
    parser = argparse.ArgumentParser(prog="thicket")
    parser.add_argument("scenario", choices=list(SCENARIOS.keys()))
    args = parser.parse_args()
    decision = SCENARIOS[args.scenario]
    result = explore_evaluate_decide(decision)

    print(f"DECISION: {result['decision']}")
    print(f"CRITERION: {result['criterion']}\n")
    print("--- EXPLORE ---")
    for o in result["explore"]:
        print(f"\n{o['name']}")
        for p in o["pros"]:
            print(f"  + {p}")
        for c in o["cons"]:
            print(f"  - {c}")
    print("\n--- EVALUATE ---")
    for e in result["evaluate"]:
        print(f"  {e['name']}: {e['score']:.1f}/10")
    print("\n--- DECIDE ---")
    print(f"  Winner: {result['decide']['winner']}")
    print(f"  {result['decide']['justification']}")


if __name__ == "__main__":
    main()
