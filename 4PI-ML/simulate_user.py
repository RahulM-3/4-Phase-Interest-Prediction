import random
import pandas as pd
import json

PHASE_ORDER = [
    "Curiosity Activation",
    "Engagement Sustainment",
    "Personal Relevance Formation",
    "Passion-Driven Mastery"
]

DOMAINS = ["STEM", "Arts", "Business", "Health"]

DOMAIN_MAP = {
    "STEM": "STEM",
    "Arts & Creative Expression": "Arts",
    "Business, Economics & Entrepreneurship": "Business",
    "Health, Medicine & Life Sciences": "Health"
}

def simulate_user_responses(user_id, selected_questions):
    user_answers = []
    domain_phase_counts = {domain: {phase: 0 for phase in PHASE_ORDER} for domain in DOMAINS}

    option_labels = ["A", "B", "C", "D"]

    for q in selected_questions:
        choice_index = random.randint(0, len(q["options"]) - 1)
        choice = q["options"][choice_index]
        user_answers.append(option_labels[choice_index])

        for domain, score in choice["domains"].items():
            if score > 0:
                mapped = DOMAIN_MAP[domain]
                domain_phase_counts[mapped][q["interest_phase"]] += 1

    flattened_counts = []
    for domain in DOMAINS:
        for phase in PHASE_ORDER:
            flattened_counts.append(domain_phase_counts[domain][phase])

    record = [user_id] + user_answers + flattened_counts
    return record

with open("questions_puller/pulled_questions.json", "r", encoding="utf-8") as f:
    pulled_questions = json.load(f)

def simulate_user():
    user_id = "TestUser"
    return simulate_user_responses(user_id, pulled_questions)