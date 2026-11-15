"""
Thicket: a small, deterministic explore-evaluate-decide decision-tree tool.
Takes a decision, a criterion, and a set of pre-described options (each with
pros, cons, and a criterion-specific score), and mechanically produces the
three-phase structure: explored options, a pros/cons/score comparison, and a
decide step naming the winner, its margin over the runner-up, and the
specific criterion it was judged against.

DISCLOSURE: options, their pros/cons, and their scores are pre-described
input data (a disclosed, rule-based stand-in for a live model's judgment),
not computed from a live LLM call. The explore/evaluate/decide *mechanics*
below -- picking the winner, computing the margin, formatting the report --
are real, general-purpose code with no simulation in them.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Option:
    name: str
    pros: list
    cons: list
    score: float  # 0-10, score against the specific stated criterion


@dataclass(frozen=True)
class Decision:
    name: str
    criterion: str
    options: list  # list[Option]


SCENARIOS = {
    "orchestration-framework": Decision(
        name="How to orchestrate a multi-agent ticket-triage pipeline for a client demo",
        criterion=(
            "ships a working, demo-ready pipeline inside a 2-week deadline, given the "
            "team has never used any agent orchestration framework before"
        ),
        options=[
            Option(
                "LangGraph",
                pros=["Built-in graph/state management fits a multi-step triage flow naturally",
                      "Large ecosystem of examples close to this exact use case"],
                cons=["Steep learning curve for a team seeing it for the first time",
                      "Its abstractions are one more layer to debug under deadline pressure"],
                score=4.0,
            ),
            Option(
                "CrewAI",
                pros=["Simpler role-based mental model than a full graph framework",
                      "Fast to get a 2-3 agent prototype running"],
                cons=["Still a brand-new framework and set of conventions to learn from zero",
                      "Less control over state handoffs once the flow gets non-trivial"],
                score=5.0,
            ),
            Option(
                "Custom Python orchestration (no framework)",
                pros=["The team already knows plain Python well -- nothing new to learn",
                      "Full visibility into every handoff, easiest to debug fast",
                      "No framework upgrade or compatibility risk before the demo"],
                cons=["Have to hand-roll retries, state handoff, and logging",
                      "Less reusable scaffolding for the client's next multi-agent project"],
                score=8.0,
            ),
        ],
    ),
}


def explore_evaluate_decide(decision: Decision) -> dict:
    """Run the three-phase structure on a Decision and return a result dict."""
    ranked = sorted(decision.options, key=lambda o: o.score, reverse=True)
    winner = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else None
    margin = (winner.score - runner_up.score) if runner_up else None
    return {
        "decision": decision.name,
        "criterion": decision.criterion,
        "explore": [{"name": o.name, "pros": o.pros, "cons": o.cons} for o in decision.options],
        "evaluate": [{"name": o.name, "score": o.score} for o in ranked],
        "decide": {
            "winner": winner.name,
            "score": winner.score,
            "runner_up": runner_up.name if runner_up else None,
            "margin": margin,
            "justification": (
                f"{winner.name} scores {winner.score:.1f} vs. {runner_up.score:.1f} for "
                f"runner-up {runner_up.name} on this criterion specifically: {decision.criterion}."
                if runner_up else
                f"{winner.name} is the only option considered."
            ),
        },
    }
