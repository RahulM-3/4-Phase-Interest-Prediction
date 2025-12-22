import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = pd.read_csv("4PI-ML/dataset/data.csv")

question_cols = [f"Q{i}" for i in range(1, 16)]
agg_cols = [col for col in data.columns if "_" in col]
domain_targets = ['STEM', 'Arts', 'Business', 'Health']
phase_order = ['CA', 'ES', 'PR', 'PM']

ohe = OneHotEncoder(sparse_output=False)
X_questions = ohe.fit_transform(data[question_cols])
X_agg = data[agg_cols].values
X = np.hstack([X_questions, X_agg])

y = pd.DataFrame()
for domain in domain_targets:
    phase_cols = [f"{domain}_{p}" for p in phase_order]
    y[domain] = data[phase_cols].idxmax(axis=1).str.split('_').str[1]

le_dict = {}
y_encoded = pd.DataFrame()
for col in y.columns:
    le = LabelEncoder()
    y_encoded[col] = le.fit_transform(y[col])
    le_dict[col] = le

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
multi_rf = MultiOutputClassifier(rf)
multi_rf.fit(X_train, y_train)

print("\nModel Accuracy per Domain:")
for idx, domain in enumerate(domain_targets):
    y_pred = multi_rf.estimators_[idx].predict(X_test)
    acc = accuracy_score(y_test[domain], y_pred)
    print(f"{domain}: {acc:.2f}")

from simulate_user import simulate_user 
sim_user_record = simulate_user()
sim_answers = sim_user_record[1:16]
sim_df = pd.DataFrame([sim_answers], columns=question_cols)

X_sim_questions = ohe.transform(sim_df[question_cols])

X_sim_agg = np.zeros((1, len(agg_cols)))
X_sim = np.hstack([X_sim_questions, X_sim_agg])

prob_dict = {}
for idx, domain in enumerate(domain_targets):
    clf = multi_rf.estimators_[idx]
    probs = clf.predict_proba(X_sim)
    phase_labels = le_dict[domain].inverse_transform(np.arange(probs.shape[1]))
    prob_df = pd.DataFrame(probs, columns=phase_labels, index=[sim_user_record[0]])
    prob_dict[domain] = prob_df

print("\nSimulated User - Phase Probabilities per Domain:")
for domain, df in prob_dict.items():
    print(f"\nDomain: {domain}")
    print(df)

pred_phase = {domain: df.idxmax(axis=1).iloc[0] for domain, df in prob_dict.items()}
print("\nSimulated User - Predicted Phase per Domain:")
print(pred_phase)
