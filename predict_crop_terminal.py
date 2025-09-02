import os
import time
import joblib
import numpy as np
import pandas as pd
from google import genai
from google.genai import types

GOOGLE_API = "YOUR_API_KEY"

# --- 1. Rate Limiter Class ---
# This class tracks request timestamps to enforce a rate limit.
class RateLimiter:
    def __init__(self, max_requests, period_seconds):
        self.max_requests = max_requests
        self.period_seconds = period_seconds
        self.requests = []

    def _cleanup_old_requests(self):
        """Removes timestamps older than the defined period."""
        current_time = time.time()
        self.requests = [req_time for req_time in self.requests if current_time - req_time < self.period_seconds]

    def is_allowed(self):
        """Checks if a new request is allowed, and records it if so."""
        self._cleanup_old_requests()
        if len(self.requests) < self.max_requests:
            self.requests.append(time.time())
            return True
        return False

# --- 2. Gemini API Integration Function ---
def get_gemini_details(crop_name, feature):
    """
    Gets additional details for a given crop from the Gemini API.
    """
    try:
        for y in feature:
            print(str(y) + " ")
        # The API key is loaded securely from the environment variable.
        client = genai.Client(api_key=GOOGLE_API, http_options=types.HttpOptions(api_version="v1alpha"))
        prompt = f"""
        Given the following agricultural conditions:
        - Nitrogen (N) ratio in soil: {feature[0]}
        - Phosphorus (P) ratio in soil: {feature[1]}
        - Potassium (K) ratio in soil: {feature[2]}
        - Temperature: {feature[3]}°C
        - Relative Humidity: {feature[4]}%
        - pH value of soil: {feature[5]}
        - Rainfall: {feature[6]} mm
        
        Explain why {crop_name} is a suitable crop choice for these specific conditions.
        Focus on how the crop's requirements align with these soil and climate parameters.
        Provide a concise, farmer-friendly justification in one paragraph.
        Also recommend some other crop if it is more suitable and explain why too.
        """
        response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=prompt)
        return response.text
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable not set."
    except Exception as e:
        return f"Error fetching details from Gemini API: {e}"

# --- 3. Main Application Logic ---
def run_prediction_workflow():
    """
    Main function to load the model, get user input, and provide recommendations.
    """
    # Load the local crop recommendation model.
    model_filename = 'crop_model.joblib'
    try:
        model = joblib.load(model_filename)
    except FileNotFoundError:
        print(f"Error: Model file '{model_filename}' not found.")
        print("Please run 'train_model.py' first.")
        exit()

    # Initialize the rate limiter: 50 requests per hour (3600 seconds).
    limiter = RateLimiter(max_requests=50, period_seconds=3600)

    try:
        print("\n--------------------------------------------------")
        print("Enter Soil and Climate Details for Recommendation")
        print("--------------------------------------------------")
        #Data fields:
        # N - ratio of Nitrogen content in soil
        # P - ratio of Phosphorous content in soil
        # K - ratio of Potassium content in soil
        # temperature - temperature in degree Celsius
        # humidity - relative humidity in %
        # ph - ph value of the soil
        # rainfall - rainfall in mm
        feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        user_values = [float(input(f"{name.capitalize()}: ")) for name in feature_names]
        
        input_df = pd.DataFrame([user_values], columns=feature_names)
        
        # --- Local Model Prediction ---
        local_prediction = model.predict(input_df)[0].capitalize()
        print("\n--------------------------------------------------")
        print(f"Local Model Recommendation: {local_prediction}")
        print("--------------------------------------------------")

        # --- Gemini API Enrichment (with Rate Limiting) ---
        if limiter.is_allowed():
            print("Fetching additional details from Gemini...")
            gemini_info = get_gemini_details(local_prediction,user_values)
            print("\nAdditional Info:")
            print(gemini_info)
        else:
            print("\nRate limit of 50 requests per hour exceeded. Please try again later.")
        print("--------------------------------------------------")

    except ValueError:
        print("\nError: Invalid input. Please enter numerical values only.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Execution ---
if __name__ == "__main__":
    run_prediction_workflow()
