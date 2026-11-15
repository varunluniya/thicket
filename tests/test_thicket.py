from thicket.core import SCENARIOS, explore_evaluate_decide, Option, Decision


def test_orchestration_scenario_registered():
    assert "orchestration-framework" in SCENARIOS


def test_explore_lists_three_options_with_pros_and_cons():
    decision = SCENARIOS["orchestration-framework"]
    result = explore_evaluate_decide(decision)
    assert len(result["explore"]) == 3
    for o in result["explore"]:
        assert o["pros"] and o["cons"]


def test_evaluate_ranks_by_score_descending():
    decision = SCENARIOS["orchestration-framework"]
    result = explore_evaluate_decide(decision)
    scores = [e["score"] for e in result["evaluate"]]
    assert scores == sorted(scores, reverse=True)


def test_decide_names_custom_python_as_winner():
    decision = SCENARIOS["orchestration-framework"]
    result = explore_evaluate_decide(decision)
    assert result["decide"]["winner"] == "Custom Python orchestration (no framework)"


def test_decide_margin_matches_8_vs_5():
    decision = SCENARIOS["orchestration-framework"]
    result = explore_evaluate_decide(decision)
    assert result["decide"]["score"] == 8.0
    assert result["decide"]["runner_up"] == "CrewAI"
    assert result["decide"]["margin"] == 3.0


def test_justification_cites_the_stated_criterion():
    decision = SCENARIOS["orchestration-framework"]
    result = explore_evaluate_decide(decision)
    assert "2-week deadline" in result["decide"]["justification"]


def test_custom_decision_with_two_options():
    d = Decision(
        name="pick a database",
        criterion="cheapest to operate",
        options=[Option("Postgres", ["mature"], ["ops overhead"], 6.0),
                  Option("SQLite", ["zero ops"], ["no concurrent writes"], 9.0)],
    )
    result = explore_evaluate_decide(d)
    assert result["decide"]["winner"] == "SQLite"
    assert result["decide"]["margin"] == 3.0


def test_single_option_decision_has_no_runner_up():
    d = Decision(name="x", criterion="y", options=[Option("OnlyOption", ["p"], ["c"], 5.0)])
    result = explore_evaluate_decide(d)
    assert result["decide"]["runner_up"] is None
    assert result["decide"]["margin"] is None


def test_langgraph_scores_lowest():
    decision = SCENARIOS["orchestration-framework"]
    result = explore_evaluate_decide(decision)
    scores = {e["name"]: e["score"] for e in result["evaluate"]}
    assert scores["LangGraph"] == min(scores.values())
