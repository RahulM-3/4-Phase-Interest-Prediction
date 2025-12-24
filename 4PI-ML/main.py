# ml_prediction.py
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import matplotlib.pyplot as plt

# =========================
# CONFIGURATION
# =========================
domains = ["STEM", "Business, Economics & Entrepreneurship", "Arts & Creative Expression", "Health, Medicine & Life Sciences"]
phases = ["Curiosity Activation", "Engagement Sustainment",
          "Personal Relevance Formation", "Passion-Driven Mastery"]
phase_weights = {
    "Curiosity Activation": 1,
    "Engagement Sustainment": 2,
    "Personal Relevance Formation": 3,
    "Passion-Driven Mastery": 4
}
NUM_DOMAINS = len(domains)
NUM_PHASES = len(phases)

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("4PI-ML/dataset/data.csv")
X = df.iloc[:, :NUM_DOMAINS*NUM_PHASES].values
y = df.iloc[:, NUM_DOMAINS*NUM_PHASES:].values

# =========================
# TRAIN-TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# =========================
# MODEL DEFINITION
# =========================
models = {
    "LogisticRegression": MultiOutputClassifier(LogisticRegression(max_iter=500)),
    "RandomForest": MultiOutputClassifier(RandomForestClassifier(n_estimators=200))
}

# =========================
# TRAIN & COMPARE
# =========================
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="micro")
    results[name] = {"accuracy": acc, "f1": f1}
    print(f"{name}: Accuracy={acc:.3f}, F1={f1:.3f}")

best_model_name = max(results, key=lambda x: results[x]["f1"])
best_model = models[best_model_name]
print(f"\nBest model selected: {best_model_name}")

# =========================
# FUNCTION TO PREDICT USER RECORD
# =========================
def answers_to_features(answers):
    feature_vector = np.zeros(NUM_DOMAINS * NUM_PHASES)
    for domain_choice, phase_choice in answers:
        feature_vector[phase_choice * NUM_DOMAINS + domain_choice] += phase_weights[phases[phase_choice]]
    return feature_vector.reshape(1, -1)

def predict_user(answers):
    features = answers_to_features(answers)
    y_pred_prob = best_model.predict_proba(features)
    scores = np.array([p[:,1] for p in y_pred_prob]).flatten()
    return dict(zip(domains, scores))

# =========================
# RADAR CHART & EXPLANATION
# =========================
def plot_radar_chart(scores, labels, title="Domain Prediction"):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    scores = np.concatenate((list(scores), [scores[0]]))
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, scores, 'o-', linewidth=2)
    ax.fill(angles, scores, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0,1)
    ax.set_title(title)
    plt.savefig("4PI-ML/result.png")
    plt.close()

def explain_prediction(scores, labels):
    explanation = sorted(zip(labels, scores), key=lambda x: x[1], reverse=True)
    print("\nSorting Domains (High -> Low):")
    for domain, score in explanation:
        print(f"{domain}: {score:.2f}")

# =========================
# EXAMPLE USER RECORD
# =========================
from simulate_user import real_user_response, simulate_user_response

record = real_user_response(4)
my_prediction = predict_user(record[1:])
print(f"\nPredicted domain scores for {record[0]}: ", my_prediction)

plot_radar_chart(list(my_prediction.values()), domains, title="Your Domain Prediction")
explain_prediction(list(my_prediction.values()), domains)