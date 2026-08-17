# Step 1: Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from joblib import dump

# Step 2: Load and preprocess the dataset
# Replace 'your_dataset.csv' with the path to your dataset file
df = pd.read_csv("dataset.csv")
# dataset = df.sample(frac=0.9, random_state=42)
dataset = df
label_encoder = LabelEncoder()
dataset["Label_encoded"] = label_encoder.fit_transform(dataset["Label"])
dataset["Class_encoded"] = label_encoder.fit_transform(dataset["Class"])

dataset.drop("Label", axis=1, inplace=True)
dataset.drop("Class", axis=1, inplace=True)
# Assuming the dataset has columns 'Feature1', 'Feature2', ..., 'Class' (where 'Class' is 'Attack' or 'Benign')
X = dataset.drop("Class_encoded", axis=1)
y = dataset["Class_encoded"]

# Step 3: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# Print some information for debugging
print("Dataset shape:", dataset.shape)
print(dataset['Label_encoded'])
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
# Step 4: Train the XGBoost classifier
xgboost_classifier = XGBClassifier(
    n_estimators=100,  # You can adjust the number of trees
    max_depth=5,  # Limit the depth of trees
    min_child_weight=14940,  # Minimum sum of instance weight (hessian) needed in a child
    gamma=0,  # Minimum loss reduction required to make a further partition on a leaf node
    subsample=0.8,  # Fraction of samples used for fitting the trees
    colsample_bytree=0.8,  # Fraction of features used for fitting the trees
    reg_alpha=0,  # L1 regularization term on weights
    reg_lambda=1,  # L2 regularization term on weights
)  # You can adjust max_depth as needed

xgboost_classifier.fit(X_train, y_train)
print("Training complete.")

print("Evaluating the classifier...")
# Step 5: Evaluate the XGBoost classifier's performance on test data
y_pred_xgboost = xgboost_classifier.predict(X_test)
accuracy_xgboost = accuracy_score(y_test, y_pred_xgboost)
classification_report_xgboost = classification_report(y_test, y_pred_xgboost)

# Print the results for the XGBoost classifier
print("XGBoost Classifier:")
print(f"Accuracy: {accuracy_xgboost}")
print("Classification Report:")
print(classification_report_xgboost)

dump (xgboost_classifier,'C:/Users/utsav/OneDrive/Desktop/Website/Hello/Hello/savedmodels/model.joblib')
