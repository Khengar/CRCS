import numpy as np
import pandas as pd  # Import the pandas library
import joblib

# --- 1. Load the Pre-trained Model ---
model_filename = 'crop_model.joblib'
try:
    model = joblib.load(model_filename)
except FileNotFoundError:
    print(f"Error: Model file '{model_filename}' not found.")
    print("Please run the 'train_model.py' script first to create the model file.")
    exit()

# --- 2. Prediction Function ---
def get_crop_recommendation():
    """Gathers user input and returns a crop prediction using the loaded model."""
    try:
        print("\n--------------------------------------------------")
        print("Enter Soil and Climate Details for Recommendation")
        print("--------------------------------------------------")

        # Define the feature names in the exact order the model was trained on.
        feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

        # Collect user input as a list of floats.
        user_values = [
            float(input("Nitrogen (N) content in soil: ")),
            float(input("Phosphorous (P) content in soil: ")),
            float(input("Potassium (K) content in soil: ")),
            float(input("Temperature in Celsius (°C): ")),
            float(input("Relative Humidity (%): ")),
            float(input("Soil pH: ")),
            float(input("Rainfall (mm): "))
        ]

        # Create a pandas DataFrame from the user's input with the correct feature names.
        # This resolves the UserWarning.
        input_df = pd.DataFrame([user_values], columns=feature_names)

        # Make the prediction using the new DataFrame.
        prediction = model.predict(input_df)

        print("\n--------------------------------------------------")
        print(f"Recommended Crop: {prediction[0].capitalize()}")
        print("--------------------------------------------------")

    except ValueError:
        print("\nError: Invalid input. Please enter numerical values only.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- 3. Execution ---
if __name__ == "__main__":
    get_crop_recommendation()