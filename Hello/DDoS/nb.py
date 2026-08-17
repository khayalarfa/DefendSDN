# Step 1: Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB  # Add Naive Bayes
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Step 2: Load and preprocess the dataset
# Replace 'your_dataset.csv' with the path to your dataset file
df = pd.read_csv("dataset.csv")
dataset = df.sample(frac=0.1, random_state=42)
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
# Naive Bayes
nb_classifier = MultinomialNB()
nb_classifier.fit(X_train, y_train)

# Step 5: Evaluate the classifiers' performance
print("Training complete.")

print("Evaluating the classifier...")
# Naive Bayes
y_pred_nb = nb_classifier.predict(X_test)
accuracy_nb = accuracy_score(y_test, y_pred_nb)
classification_report_nb = classification_report(y_test, y_pred_nb)

# Print the results

print("\nNaive Bayes Classifier:")
print(f"Accuracy: {accuracy_nb}")
print("Classification Report:")
print(classification_report_nb)
