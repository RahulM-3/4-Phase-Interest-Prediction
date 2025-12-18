import pandas as pd
import numpy as np
import random

# ----------------------------
# Parameters
# ----------------------------
num_users = 50
num_questions = 15
options = ['A', 'B', 'C', 'D']
domains = ['STEM', 'Arts', 'Business', 'Health']
phases = ['CA', 'ES', 'PR', 'PM']

# Mapping options to domains randomly (for synthetic data)
option_domain_map = {
    'A': 'STEM',
    'B': 'Arts',
    'C': 'Business',
    'D': 'Health'
}

# ----------------------------
# Generate question-level responses
# ----------------------------
data = []
for user_id in range(1, num_users + 1):
    row = {}
    row['UserID'] = f'U{user_id}'
    # Randomly select options for each question
    for q in range(1, num_questions + 1):
        row[f'Q{q}'] = random.choice(options)
    data.append(row)

df = pd.DataFrame(data)

# ----------------------------
# Generate aggregated domain-phase counts
# ----------------------------
for domain in domains:
    for phase in phases:
        # Random counts between 0 and 3 for synthetic data
        df[f'{domain}_{phase}'] = np.random.randint(0, 4, size=num_users)

# ----------------------------
# Save to CSV
# ----------------------------
df.to_csv("4PI-ML/dataset/data.csv", index=False)
print("50-user synthetic dataset generated: sample_interest_dataset_50.csv")
