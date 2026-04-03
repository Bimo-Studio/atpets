import csv
import random
from collections import defaultdict

# --- config ---
CSV_PATH = "atpets.csv"
SEED = 42
N = 10  # number of outputs

random.seed(SEED)

# --- load traits ---
traits = defaultdict(list)

with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        traits[row["category"]].append(
            (row["value"], float(row["weight"]))
        )

# --- weighted choice ---
def weighted_choice(options):
    values, weights = zip(*options)
    return random.choices(values, weights=weights, k=1)[0]

# --- constraint logic ---
def apply_constraints(selected):
    # example constraints (you will need more)
    
    # floating body shouldn't have "standing"
    if selected["body"] == "floating":
        selected["pose"] = "hovering"
    
    # gelatinous + fur conflict
    if selected["skin"] == "gelatinous":
        selected["tail"] = "none"
    
    # none cleanup
    for k, v in selected.items():
        if v == "none":
            selected[k] = None
    
    return selected

# --- prompt builder ---
def build_prompt(traits):
    parts = []

    parts.append("cute original creature, clean vector style, thick outlines")
    parts.append("centered character sheet style, white background")

    # structured trait injection
    if traits["body"]:
        parts.append(traits["body"] + " body")
    if traits["skin"]:
        parts.append(traits["skin"] + " texture")

    # colors
    color_str = traits["color_primary"]
    if traits["color_secondary"]:
        color_str += " and " + traits["color_secondary"]
    parts.append(color_str + " color palette")

    # anatomy
    for key in ["eyes", "ears", "tail"]:
        if traits[key]:
            parts.append(traits[key])

    # extras
    if traits["special"]:
        parts.append(traits["special"])

    # pose + expression
    parts.append(traits["pose"] + " pose")
    parts.append(traits["expression"] + " expression")

    # model guidance (important for consistency)
    parts.append("flat shading, minimal gradients, no background clutter")
    parts.append("consistent style, no text, no watermark")

    return ", ".join(parts)

# --- generation loop ---
def generate(n):
    outputs = []

    for i in range(n):
        selected = {}

        for category in traits:
            selected[category] = weighted_choice(traits[category])

        selected = apply_constraints(selected)

        prompt = build_prompt(selected)

        outputs.append({
            "id": i,
            "traits": selected,
            "prompt": prompt
        })

    return outputs

# --- run ---
results = generate(N)

for r in results:
    print(f"\nID {r['id']}")
    print("TRAITS:", r["traits"])
    print("PROMPT:", r["prompt"])
