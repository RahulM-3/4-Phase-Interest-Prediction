import os
import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

folder_path = "questions"
summary_base = os.path.join(folder_path, "summary")
os.makedirs(summary_base, exist_ok=True)

age_groups = ["primary", "secondary", "highered", "lifelong"]
age_group_data = {}

# Load JSON data
for age_group in age_groups:
    json_file = os.path.join(folder_path, age_group, f"{age_group}.json")
    if not os.path.exists(json_file):
        print(f"JSON file not found: {json_file}")
        continue
    with open(json_file, "r", encoding="utf-8") as f:
        age_group_data[age_group] = json.load(f)

summary_rows = []

# Analyze each age group
for age_group, questions in age_group_data.items():
    print(f"\n=== Analysis for {age_group} ===")
    
    phase_counter = Counter()
    domain_counter = Counter()
    phase_domain_counts = defaultdict(lambda: Counter())
    
    for q in questions:
        phase = q["interest_phase"]
        phase_counter[phase] += 1
        for opt in q["options"]:
            non_neutral_domains = [d for d in opt["domains"] if d != "Neutral"]
            for domain in non_neutral_domains:
                domain_counter[domain] += 1
                phase_domain_counts[phase][domain] += 1
    
    # Print Phase distribution
    print("Phase distribution:")
    for phase, count in phase_counter.items():
        print(f"  {phase}: {count}")
    
    # Print Domain distribution
    print("Domain distribution:")
    for domain, count in domain_counter.items():
        print(f"  {domain}: {count}")
    
    # Check domain balance
    warnings = []
    if domain_counter:
        total_domains = len(domain_counter)
        if total_domains < 4:
            warnings.append("Some domains are missing.")
            print("Some domains are missing.")
        max_count = max(domain_counter.values())
        min_count = min(domain_counter.values())
        if max_count > 2 * min_count:
            warnings.append("Domain counts are highly imbalanced.")
            print("Domain counts are highly imbalanced.")
    
    # Ensure summary folder exists
    summary_folder = os.path.join(summary_base, age_group)
    os.makedirs(summary_folder, exist_ok=True)
    
    # Plot Phase distribution
    plt.figure(figsize=(8, 4))
    plt.bar(phase_counter.keys(), phase_counter.values(), color='skyblue')
    plt.title(f"{age_group} - Questions per Phase")
    plt.xlabel("Phase")
    plt.ylabel("Number of Questions")
    plt.savefig(os.path.join(summary_folder, "Questions_per_Phase.png"), dpi=300)
    plt.close()
    
    # Plot Domain distribution
    plt.figure(figsize=(8, 4))
    plt.bar(domain_counter.keys(), domain_counter.values(), color='lightgreen')
    plt.title(f"{age_group} - Option Distribution per Domain")
    plt.xlabel("Domain")
    plt.ylabel("Option Counts")
    plt.savefig(os.path.join(summary_folder, "Option_Distribution_per_Domain.png"), dpi=300)
    plt.close()
    
    # Heatmap Phase vs Domain
    phases = list(phase_domain_counts.keys())
    domains = sorted({d for ph in phases for d in phase_domain_counts[ph].keys()})
    heatmap_data = [[phase_domain_counts[ph].get(d, 0) for d in domains] for ph in phases]
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt="d", xticklabels=domains, yticklabels=phases, cmap="YlGnBu")
    plt.title(f"{age_group} - Phase vs Domain Option Count")
    plt.xlabel("Domain")
    plt.ylabel("Phase")
    plt.savefig(os.path.join(summary_folder, "Phase_vs_Domain_Option_Count.png"), dpi=300)
    plt.close()
        
    # Save Domain distribution as separate chart for easier visualization
    plt.figure(figsize=(8, 4))
    sns.barplot(
        x=list(domain_counter.keys()),
        y=list(domain_counter.values()),
        hue=list(domain_counter.keys()),
        palette="pastel",
        legend=False
    )
    plt.title(f"{age_group} - Overall Domain Distribution")
    plt.xlabel("Domain")
    plt.ylabel("Option Counts")
    plt.savefig(os.path.join(summary_folder, "Overall_Domain_Distribution.png"), dpi=300)
    plt.close()
    
    # Prepare summary dataframe
    for phase in phases:
        for domain in domains:
            summary_rows.append({
                "Age Group": age_group,
                "Phase": phase,
                "Domain": domain,
                "Option Count": phase_domain_counts[phase].get(domain, 0),
                "Warnings": "; ".join(warnings)
            })

# Save overall summary
summary_df = pd.DataFrame(summary_rows)
summary_csv = os.path.join(summary_base, "question_analysis_summary.csv")
summary_df.to_csv(summary_csv, index=False)
print(f"\nSummary CSV saved: {summary_csv}")