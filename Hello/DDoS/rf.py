# Step 1: Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Step 2: Load and preprocess the dataset
# Replace 'your_dataset.csv' with the path to your dataset file
df = pd.read_csv("dataset.csv")
dataset = df.sample(frac=0.8, random_state=42)
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
random_forest_classifier = RandomForestClassifier(
    n_estimators=100,  # You can adjust the number of trees
    max_depth=10,  # Limit the depth of trees
    min_samples_leaf=50000,  # Set minimum samples per leaf
    max_features="sqrt",  # Set max features to "sqrt" or "log2"
)  # You can adjust hyperparameters as needed
random_forest_classifier.fit(X_train, y_train)

# Step 5: Evaluate the classifiers' performance
print("Training complete.")

print("Evaluating the classifier...")
y_pred_rf = random_forest_classifier.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
classification_report_rf = classification_report(y_test, y_pred_rf)

# Print the results

print("\nRandom Forest Classifier:")
print(f"Accuracy: {accuracy_rf}")
print("Classification Report:")
print(classification_report_rf)
