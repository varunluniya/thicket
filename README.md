# Thicket

A small, tested explore-evaluate-decide decision-tree tool. Give it a
decision, a specific criterion, and a set of pre-described options (each
with pros, cons, and a criterion-specific score), and it mechanically
produces the three-phase structure: explored options, a ranked
pros/cons/score comparison, and a decide step that names the winner, its
margin over the runner-up, and the exact criterion it was judged against.

**Disclosure:** option pros/cons/scores are pre-described input data — a
disclosed, rule-based stand-in for a live model's judgment, not a live LLM
call. The explore/evaluate/decide mechanics (ranking, margin computation,
report formatting) are real, general-purpose code.

## Usage

```bash
pip install -e .
python -m thicket.cli orchestration-framework
```

```python
from thicket import Option, Decision, explore_evaluate_decide

d = Decision(
    name="pick a database", criterion="cheapest to operate",
    options=[Option("Postgres", ["mature"], ["ops overhead"], 6.0),
             Option("SQLite", ["zero ops"], ["no concurrent writes"], 9.0)],
)
result = explore_evaluate_decide(d)
# result["decide"]["winner"] == "SQLite"
```

## Why decision-tree structure beats a bare "what should I use" prompt

Forcing Explore as its own step surfaces options a bare recommendation
would never propose (a "no framework" answer to "which framework"). Making
Evaluate its own step keeps the comparison criterion-specific rather than
generic. And because Decide's justification names the exact criterion and
margin, the recommendation is traceable — you can point to the sentence
that ties the pick to the stated constraint.

## Tests

```bash
pytest -v
```

9/9 passing.

## License

MIT
