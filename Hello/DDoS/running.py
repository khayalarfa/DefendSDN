import joblib

# Specify the path where you saved the model
model_file_path = 'savedmodel.joblib'

# Load the saved model
loaded_model = joblib.load(model_file_path)

# Now, you can use the loaded model for predictions
new_data_point = [[6, 10125077, 2238, 562, 0, 139.875, 341.33075, 2.9629405, 10100275, 1.5802349, 0, 562, 111.48387 , 1, 115.2, 139.875, 2238, 0]]
prediction = loaded_model.predict(new_data_point)

print("Prediction:", prediction)


																
