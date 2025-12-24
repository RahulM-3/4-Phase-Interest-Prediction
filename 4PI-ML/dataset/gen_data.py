import numpy as np
import pandas as pd

# =========================
# CONFIGURATION
# =========================
NUM_USERS = 1000
NUM_QUESTIONS = 15
NUM_DOMAINS = 4
NUM_PHASES = 4

domains = ["STEM", "Business, Economics & Entrepreneurship", "Arts & Creative Expression", "Health, Medicine & Life Sciences"]
phases = ["Curiosity Activation", "Engagement Sustainment",
          "Personal Relevance Formation", "Passion-Driven Mastery"]

phase_weights = {
    "Curiosity Activation": 1,
    "Engagement Sustainment": 2,
    "Personal Relevance Formation": 3,
    "Passion-Driven Mastery": 4
}

# =========================
# FUNCTIONS
# =========================
def generate_user_answer():
    answers = []
    for _ in range(NUM_QUESTIONS):
        domain_choice = np.random.randint(0, NUM_DOMAINS)
        phase_choice = np.random.randint(0, NUM_PHASES)
        answers.append((domain_choice, phase_choice))
    return answers

def answers_to_features(answers):
    feature_vector = np.zeros(NUM_DOMAINS * NUM_PHASES)
    for domain_choice, phase_choice in answers:
        feature_vector[phase_choice * NUM_DOMAINS + domain_choice] += phase_weights[phases[phase_choice]]
    return feature_vector

def generate_target_domains(answers):
    domain_scores = np.zeros(NUM_DOMAINS)
    for domain_choice, phase_choice in answers:
        domain_scores[domain_choice] += phase_weights[phases[phase_choice]]
    top_indices = domain_scores.argsort()[-2:]  # pick top 2 domains
    target = np.zeros(NUM_DOMAINS)
    target[top_indices] = 1
    return target

# =========================
# GENERATE DATASET
# =========================
X_list, y_list = [], []
for _ in range(NUM_USERS):
    ans = generate_user_answer()
    X_list.append(answers_to_features(ans))
    y_list.append(generate_target_domains(ans))

X_array = np.array(X_list)
y_array = np.array(y_list)

# Combine features and targets into a single CSV
df_features = pd.DataFrame(X_array, columns=[f"F{i+1}" for i in range(NUM_DOMAINS*NUM_PHASES)])
df_targets = pd.DataFrame(y_array, columns=domains)
df = pd.concat([df_features, df_targets], axis=1)
df.to_csv("4PI-ML/dataset/data.csv", index=False)

print("Synthetic dataset generated")