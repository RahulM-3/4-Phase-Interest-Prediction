import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
import numpy as np

# ----------------------------
# 1. Load Dataset
# ----------------------------
data = pd.read_csv("4PI-ML/dataset/data.csv")

# Question columns
question_cols = [f"Q{i}" for i in range(1, 16)]

# Aggregated features (optional)
agg_cols = [col for col in data.columns if "_" in col]

# Domain output columns (targets)
domain_targets = ['STEM', 'Arts', 'Business', 'Health']

# ----------------------------
# 2. Encode Question Options
# ----------------------------
ohe = OneHotEncoder(sparse_output=False)
X_questions = ohe.fit_transform(data[question_cols])

# Optional aggregated features
X_agg = data[agg_cols].values
X = np.hstack([X_questions, X_agg])

# ----------------------------
# 3. Encode Targets
# ----------------------------
phase_order = ['CA', 'ES', 'PR', 'PM']
y = pd.DataFrame()
for domain in domain_targets:
    phase_cols = [f"{domain}_{p}" for p in phase_order]
    y[domain] = data[phase_cols].idxmax(axis=1).str.split('_').str[1]

# Label encoding
le_dict = {}
y_encoded = pd.DataFrame()
for col in y.columns:
    le = LabelEncoder()
    y_encoded[col] = le.fit_transform(y[col])
    le_dict[col] = le

# ----------------------------
# 4. Split Data
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# ----------------------------
# 5. Train Random Forest Multi-Output
# ----------------------------
rf = RandomForestClassifier(n_estimators=100, random_state=42)
multi_rf = MultiOutputClassifier(rf)
multi_rf.fit(X_train, y_train)

# ----------------------------
# 6. Make Predictions with Probabilities
# ----------------------------
prob_dict = {}
for idx, domain in enumerate(domain_targets):
    clf = multi_rf.estimators_[idx]  # RandomForest for this domain
    probs = clf.predict_proba(X_test)  # shape: (n_samples, n_classes)
    
    # Convert to DataFrame with phase labels
    phase_labels = le_dict[domain].inverse_transform(np.arange(probs.shape[1]))
    prob_df = pd.DataFrame(probs, columns=phase_labels, index=[f"User{i}" for i in range(len(probs))])
    
    prob_dict[domain] = prob_df

# Display probabilities
for domain, df in prob_dict.items():
    print(f"\nDomain: {domain}")
    print(df)

# Optional: Most likely phase per domain
pred_phase_df = pd.DataFrame({domain: df.idxmax(axis=1) for domain, df in prob_dict.items()})
print("\nPredicted Phase per Domain:")
print(pred_phase_df)

