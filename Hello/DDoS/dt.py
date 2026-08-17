# Step 1: Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier  # Add Decision Tree
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Step 2: Load and preprocess the dataset
# Replace 'your_dataset.csv' with the path to your dataset file
df = pd.read_csv("dataset.csv")
dataset = df.sample(frac=0.99, random_state=42)
# Assuming 'StringFeature' is the name of your string feature column
label_encoder = LabelEncoder()
dataset["Label_encoded"] = label_encoder.fit_transform(dataset["Label"])

# Remove the original 'StringFeature' column if you no longer need it
dataset.drop("Label", axis=1, inplace=True)
# Assuming the dataset has columns 'Feature1', 'Feature2', ..., 'Class' (where 'Class' is 'Attack' or 'Benign')
X = dataset.drop("Class", axis=1)
y = dataset["Class"]

# Step 3: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# Print some information for debugging
print("Dataset shape:", dataset.shape)
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
# Step 4: Train the Decision Tree classifier
decision_tree_classifier = DecisionTreeClassifier(
    max_depth=3, min_samples_leaf=95000
)  # You can adjust hyperparameters as needed

cross_val_scores = cross_val_score(decision_tree_classifier, X, y, cv=5)

# Print cross-validation results
print("Cross-Validation Scores:")
print(cross_val_scores)
print(f"Average Accuracy: {cross_val_scores.mean()}")

decision_tree_classifier.fit(X_train, y_train)

print("Training complete.")

print("Evaluating the classifier...")
# Step 5: Evaluate the Decision Tree classifier's performance
y_pred_decision_tree = decision_tree_classifier.predict(X_test)
accuracy_decision_tree = accuracy_score(y_test, y_pred_decision_tree)
classification_report_decision_tree = classification_report(
    y_test, y_pred_decision_tree
)

# Print the results for the Decision Tree classifier
print("Decision Tree Classifier:")
print(f"Accuracy: {accuracy_decision_tree}")
print("Classification Report:")
print(classification_report_decision_tree)
