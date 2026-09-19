from pathlib import Path

p = Path("catalog/services/recommendations.py")
s = p.read_text(encoding="utf-8")

mapping = '''
GOAL_TO_DEVELOPMENT_AREAS = {
    "\u0645\u0647\u0627\u0631\u062a \u062d\u0631\u06a9\u062a\u06cc": {
        "\u062d\u0631\u06a9\u062a\u06cc \u0638\u0631\u06cc\u0641",
        "\u062d\u0631\u06a9\u062a\u06cc \u062f\u0631\u0634\u062a",
        "\u0645\u0647\u0627\u0631\u062a \u062d\u0631\u06a9\u062a\u06cc \u0638\u0631\u06cc\u0641",
        "\u0645\u0647\u0627\u0631\u062a \u062d\u0631\u06a9\u062a\u06cc \u062f\u0631\u0634\u062a",
        "\u0647\u0645\u0627\u0647\u0646\u06af\u06cc \u0686\u0634\u0645 \u0648 \u062f\u0633\u062a",
    },
    "\u0645\u0647\u0627\u0631\u062a \u0627\u062c\u062a\u0645\u0627\u0639\u06cc": {
        "\u0627\u062c\u062a\u0645\u0627\u0639\u06cc",
        "\u0628\u0627\u0632\u06cc \u0646\u0645\u0627\u062f\u06cc\u0646",
    },
    "\u062e\u0644\u0627\u0642\u06cc\u062a": {
        "\u062e\u0644\u0627\u0642\u06cc\u062a",
    },
    "\u06cc\u0627\u062f\u06af\u06cc\u0631\u06cc": {
        "\u0634\u0646\u0627\u062e\u062a\u06cc",
        "\u062d\u0644 \u0645\u0633\u0626\u0644\u0647",
        "\u062a\u0645\u0631\u06a9\u0632 \u0648 \u062a\u0648\u062c\u0647",
        "\u0632\u0628\u0627\u0646 \u0648 \u0648\u0627\u0698\u06af\u0627\u0646",
        "\u0632\u0628\u0627\u0646 \u0648 \u0627\u0631\u062a\u0628\u0627\u0637",
    },
}

def get_goal_area_matches(goals, development_names):
    normalized_areas = set(development_names)
    matches = []
    for goal in goals:
        mapped_areas = GOAL_TO_DEVELOPMENT_AREAS.get(goal, set())
        if normalized_areas.intersection(mapped_areas):
            matches.append(goal)
    return matches
'''

marker = "def recommend_for_child(child, limit: int = 5):"

if "GOAL_TO_DEVELOPMENT_AREAS" in s:
    raise SystemExit("MAPPING_ALREADY_EXISTS")

s = s.replace(marker, mapping + "\n\n" + marker, 1)

old = '''        matched_goals = [
            goal
            for goal in goals
            if any(
                goal in area or area in goal
                for area in development_names
            )
        ]'''

new = '''        matched_goals = get_goal_area_matches(
            goals,
            development_names,
        )'''

if old not in s:
    raise SystemExit("TOY_MATCH_BLOCK_NOT_FOUND")

s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")
print("PATCH_OK")
