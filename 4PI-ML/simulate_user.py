import random
import csv
import json

PHASE_ORDER = [
    "Curiosity Activation",
    "Engagement Sustainment",
    "Personal Relevance Formation",
    "Passion-Driven Mastery"
]

DOMAINS = ["STEM", "Business", "Arts", "Health"]

DOMAIN_MAP = {
    "STEM": "STEM",
    "Business, Economics & Entrepreneurship": "Business",
    "Arts & Creative Expression": "Arts",
    "Health, Medicine & Life Sciences": "Health"
}


def simulate_user_response():
    """
    Generate a random user record as a list of (domain_index, phase_index) tuples
    """
    record = ["SyntUser"]
    for _ in range(15):
        domain_idx = random.randint(0, len(DOMAINS)-1)
        phase_idx = random.randint(0, len(PHASE_ORDER)-1)
        record.append((domain_idx, phase_idx))
    return record

def csv_row_to_ml_record(row):
    """
    Convert a CSV row (Name + answers) into a list of (domain_index, phase_index) tuples
    by matching the answer text to the JSON option text.
    """
    # Load question bank
    with open("questions_puller/pulled_questions.json", "r", encoding="utf-8") as f:
        question_bank = json.load(f)
        question_lookup = {q["question"].strip(): q for q in question_bank}

    my_answers = [row["Name"].strip()]
    answer_texts = [row[q].strip() for q in row if q != "Name"]  # skip Name

    for i, selected_text in enumerate(answer_texts):
        # Match question
        question_text = list(question_lookup.keys())[i]
        q = question_lookup[question_text]

        # Find which option matches the answer text
        option_found = None
        for opt in q["options"]:
            if opt["text"].strip() == selected_text.strip():
                option_found = opt
                break

        if option_found is None:
            # If no match, fallback to first option
            print(f"⚠️ Answer not found for question: {question_text}, using first option")
            option_found = q["options"][0]

        # Get domain index (first domain with score>0)
        domain_name = None
        for dom, score in option_found["domains"].items():
            if score > 0:
                domain_name = dom
                break
        if domain_name is None:
            domain_idx = 0
        else:
            domain_idx = DOMAINS.index(DOMAIN_MAP[domain_name])

        # Phase index
        phase_idx = PHASE_ORDER.index(q["interest_phase"])

        my_answers.append((domain_idx, phase_idx))

    return my_answers


def real_user_response(userIndex):
    csv_file = "4PI-ML/4PI.csv"
    records = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = csv_row_to_ml_record(row)
            records.append(record)
    return records[userIndex]


# Example usage
if(__name__ == "__main__"):
    print("Random record:", simulate_user_response())
    print("User record:", real_user_response(0))