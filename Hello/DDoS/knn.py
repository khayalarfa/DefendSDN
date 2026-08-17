  # Step 1: Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Step 2: Load and preprocess the dataset
# Replace 'your_dataset.csv' with the path to your dataset file
df = pd.read_csv("dataset.csv")
dataset = df.sample(frac=0.1, random_state=42)
# Assuming 'StringFeature' is the name of your string feature column
label_encoder = LabelEncoder()
dataset["Label_encoded"] = label_encoder.fit_transform(dataset["Label"])
dataset["Class_encoded"] = label_encoder.fit_transform(dataset["Class"])
# Remove the original 'StringFeature' column if you no longer need it
dataset.drop("Label", axis=1, inplace=True)
dataset.drop("Class", axis=1, inplace=True)
# Assuming the dataset has columns 'Feature1', 'Feature2', ..., 'Class' (where 'Class' is 'Attack' or 'Benign')
X = dataset.drop("Class_encoded", axis=1)
y = dataset["Class_encoded"]

# Step 3: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
X_test = X_test.astype(float)

# Step 4: Train the KNN classifier
knn_classifier = KNeighborsClassifier(
    n_neighbors=2
)  # You can adjust the number of neighbors (k)
knn_classifier.fit(X_train, y_train)

# Step 5: Evaluate the KNN classifier's performance
y_pred_knn = knn_classifier.predict(X_test)
accuracy_knn = accuracy_score(y_test, y_pred_knn)
classification_report_knn = classification_report(y_test, y_pred_knn)

# Print the results for the KNN classifier
print("KNN Classifier:")
print("Accuracy: {accuracy_knn}")
print("Classification Report:")
print(classification_report_knn)
