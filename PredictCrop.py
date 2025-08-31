import os
import time
import joblib
import numpy as np
import pandas as pd
from google import genai
from google.genai import types

GOOGLE_API = "AIzaSyC4j8QeulQ-fx5DZYy0VS2VcS-egWVfb5A"

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
def run_prediction_workflow(user_values):
    """
    Main function to load the model, get user input, and provide recommendations.
    """
    # Load the local crop recommendation model.

    local_prediction = ""
    gemini_info = ""
    error = ""

    model_filename = 'crop_model.joblib'
    try:
        model = joblib.load(model_filename)
    except FileNotFoundError:
        error = f"Error: Model file '{model_filename}' not found."
        return local_prediction, gemini_info, error

    # Initialize the rate limiter: 50 requests per hour (3600 seconds).
    limiter = RateLimiter(max_requests=50, period_seconds=3600)

    try:
        feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        # user_values = [float(input(f"{name.capitalize()}: ")) for name in feature_names]
        
        input_df = pd.DataFrame([user_values], columns=feature_names)
        
        # --- Local Model Prediction ---
        local_prediction = model.predict(input_df)[0].capitalize()

        # --- Gemini API Enrichment (with Rate Limiting) ---
        if limiter.is_allowed():
            gemini_info = get_gemini_details(local_prediction,user_values)
        else:
            gemini_info = "Rate limit of 50 requests per hour exceeded. Please try again later."

    except ValueError:
        error = "Error: Invalid input. Please enter numerical values only."
    except Exception as e:
        error = "An unexpected error occurred: {e}"
    return local_prediction, gemini_info, error

# --- Execution ---
if __name__ == "__main__":
    run_prediction_workflow()