import json
import random
import numpy as np
from collections import Counter, defaultdict
from utils import *

def load_questions(age_group):
    filename = f"questions/{age_group}.json"
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_pulled_questions(questions):
    shuffled_questions = []

    for q in questions:
        q_copy = q.copy()
        options_copy = q["options"].copy()
        random.shuffle(options_copy)
        q_copy["options"] = options_copy
        shuffled_questions.append(q_copy)

    output_path = f"questions_puller/pulled_questions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(shuffled_questions, f, indent=2, ensure_ascii=False)

    print(f"\nPulled questions saved to: {output_path}")

def compute_phase_counts(age_group, total_q=15):
    weights = PHASE_WEIGHTS[age_group]
    total_weight = sum(weights.values())

    phase_counts = {
        phase: round((w / total_weight) * total_q)
        for phase, w in weights.items()
    }

    while sum(phase_counts.values()) != total_q:
        diff = total_q - sum(phase_counts.values())
        dominant = max(weights, key=weights.get)
        phase_counts[dominant] += diff

    return phase_counts

def pull_questions(age_group, total_q=15):
    questions = load_questions(age_group)
    phase_sequence = PHASE_SEQUENCES[age_group]

    phase_pools = defaultdict(list)
    for q in questions:
        phase_pools[q["interest_phase"]].append(q)

    for phase in phase_pools:
        random.shuffle(phase_pools[phase])

    selected = []

    phase_used_count = Counter()

    for phase in phase_sequence:
        if phase_used_count[phase] >= len(phase_pools[phase]):
            raise ValueError(f"Not enough questions for phase: {phase}")

        selected.append(phase_pools[phase][phase_used_count[phase]])
        phase_used_count[phase] += 1

    return selected

def analyze_questions(selected_questions):
    phase_dist = Counter(q["interest_phase"] for q in selected_questions)
    ordered_phase_dist = {p: phase_dist.get(p, 0) for p in PHASE_ORDER}

    domain_dist = Counter()
    phase_domain_matrix = defaultdict(lambda: Counter())

    for q in selected_questions:
        phase = q["interest_phase"]
        for opt in q["options"]:
            for domain, score in opt["domains"].items():
                if score > 0:
                    mapped = DOMAIN_MAP[domain]
                    domain_dist[mapped] += 1
                    phase_domain_matrix[phase][mapped] += 1

    domain_dist = {d: domain_dist.get(d, 0) for d in DOMAINS}

    domain_std = np.std(list(domain_dist.values()))
    domain_bias = domain_std > 2.0

    dominant_phase = max(ordered_phase_dist, key=ordered_phase_dist.get)

    thresholds = {}
    threshold_flags = {}

    for domain in DOMAINS:
        n = max(1, domain_dist[domain] // 4)

        thresholds[domain] = {
            "Curiosity Activation": 1,
            "Engagement Sustainment": 1,
            "Personal Relevance Formation": 2,
            "Passion-Driven Mastery": 3
        }

        threshold_flags[domain] = {
            "pm_reachable": n >= thresholds[domain]["Passion-Driven Mastery"]
        }

    curiosity_heavy = ordered_phase_dist["Curiosity Activation"] > (
        ordered_phase_dist["Personal Relevance Formation"] +
        ordered_phase_dist["Passion-Driven Mastery"]
    )

    mastery_heavy = ordered_phase_dist["Passion-Driven Mastery"] > ordered_phase_dist["Curiosity Activation"]

    phase_unique_questions = {
        phase: len({q["question"] for q in selected_questions if q["interest_phase"] == phase})
        for phase in PHASE_ORDER
    }

    redundancy_risk = any(
        phase_unique_questions[p] < ordered_phase_dist[p]
        for p in PHASE_ORDER
    )

    return {
        "phase_distribution": ordered_phase_dist,
        "domain_distribution": domain_dist,
        "phase_domain_matrix": {
            p: dict(phase_domain_matrix[p]) for p in PHASE_ORDER
        },
        "domain_bias_detected": domain_bias,
        "dominant_phase": dominant_phase,
        "domain_phase_thresholds": thresholds,
        "threshold_reachability": threshold_flags,
        "curiosity_heavy_dataset": curiosity_heavy,
        "mastery_heavy_dataset": mastery_heavy,
        "redundancy_risk_detected": redundancy_risk
    }

age_group = "highered"  # primary / secondary / highered / lifelong

selected = pull_questions(age_group)
save_pulled_questions(selected)
insights = analyze_questions(selected)

print("\nAGE GROUP:", age_group.upper())
print("Phase Distribution:", insights["phase_distribution"])
print("Domain Distribution:", insights["domain_distribution"])
print("Domain Bias Detected:", insights["domain_bias_detected"])
print("Dominant Phase:", insights["dominant_phase"])

print("\nPhase x Domain Matrix:")
for phase, domains in insights["phase_domain_matrix"].items():
    print(phase, ":", domains)

print("\nDomain - Phase Thresholds (minimum):")
for domain, t in insights["domain_phase_thresholds"].items():
    print(domain, ":", t, "| PM Reachable:", insights["threshold_reachability"][domain]["pm_reachable"])

print("\nDataset Flags:")
print("Curiosity Heavy Dataset:", insights["curiosity_heavy_dataset"])
print("Mastery Heavy Dataset:", insights["mastery_heavy_dataset"])
print("Redundancy Risk Detected:", insights["redundancy_risk_detected"])