import os
import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

BASE_FOLDER = "questions"
SUMMARY_BASE = os.path.join(BASE_FOLDER, "summary")
os.makedirs(SUMMARY_BASE, exist_ok=True)

AGE_GROUPS = ["primary", "secondary", "highered", "lifelong"]

def truncate(text, max_len=12):
    return text if len(text) <= max_len else text[:max_len - 1] + "…"

summary_rows = []

for age_group in AGE_GROUPS:
    json_path = os.path.join(BASE_FOLDER, age_group, f"{age_group}.json")
    if not os.path.exists(json_path):
        print(f"❌ Missing: {json_path}")
        continue

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions = data  

    print(f"\n=== Analysis for {age_group.upper()} ===")

    phase_counter = Counter()
    domain_counter = Counter()
    phase_domain = defaultdict(Counter)

    for q in questions:
        phase = q["interest_phase"]
        phase_counter[phase] += 1

        for opt in q["options"]:
            for domain, score in opt["domains"].items():
                if domain == "Neutral":
                    continue
                domain_counter[domain] += score
                phase_domain[phase][domain] += score

    # ---- Console Output ----
    print("\nPhase distribution:")
    for p, c in phase_counter.items():
        print(f"  {p}: {c}")

    print("\nDomain distribution:")
    for d, c in domain_counter.items():
        print(f"  {d}: {c}")

    print("\nDomains per phase:")
    for p, dmap in phase_domain.items():
        print(f"  {p}:")
        for d, c in dmap.items():
            print(f"    - {d}: {c}")

    # ---- Warnings ----
    warnings = []
    if domain_counter:
        vals = list(domain_counter.values())
        if max(vals) > 2 * min(vals):
            warnings.append("Domain imbalance detected")

    # ---- Prepare folders ----
    summary_folder = os.path.join(SUMMARY_BASE, age_group)
    os.makedirs(summary_folder, exist_ok=True)

    # ---- Phase chart ----
    plt.figure(figsize=(8, 4))
    plt.bar(phase_counter.keys(), phase_counter.values())
    plt.title(f"{age_group} – Questions per Phase")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(summary_folder, "questions_per_phase.png"), dpi=300)
    plt.close()

    # ---- Domain chart ----
    plt.figure(figsize=(8, 4))
    plt.bar(domain_counter.keys(), domain_counter.values())
    plt.title(f"{age_group} – Domain Distribution")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(summary_folder, "domain_distribution.png"), dpi=300)
    plt.close()

    # ---- Heatmap ----
    phases = list(phase_domain.keys())
    domains = sorted(domain_counter.keys())

    heatmap = [[phase_domain[p].get(d, 0) for d in domains] for p in phases]

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        heatmap,
        annot=True,
        fmt="d",
        xticklabels=[truncate(d) for d in domains],
        yticklabels=phases,
        cmap="YlGnBu"
    )
    plt.title(f"{age_group} – Phase × Domain")
    plt.tight_layout()
    plt.savefig(os.path.join(summary_folder, "phase_vs_domain_heatmap.png"), dpi=300)
    plt.close()

    # ---- CSV rows ----
    for p in phases:
        for d in domains:
            summary_rows.append({
                "Age Group": age_group,
                "Phase": p,
                "Domain": d,
                "Score": phase_domain[p].get(d, 0),
                "Warnings": "; ".join(warnings)
            })

# ---- Save CSV ----
df = pd.DataFrame(summary_rows)
csv_path = os.path.join(SUMMARY_BASE, "question_analysis_summary.csv")
df.to_csv(csv_path, index=False)

print(f"\nSummary saved to {csv_path}")
