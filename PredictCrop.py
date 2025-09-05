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

# --- 3. Fertilizer Prediction Function ---
def predict_fertilizer(crop_name, soil_features, soil_type="Loamy"):
    """
    Predicts the best fertilizer for a given crop and soil conditions.
    
    Args:
        crop_name (str): The predicted crop name
        soil_features (list): List of [N, P, K, temperature, humidity, ph, rainfall]
        soil_type (str): Soil type (default: Loamy)
    
    Returns:
        str: Predicted fertilizer name
        str: Error message if any
    """
    try:
        # Load the fertilizer prediction model
        fertilizer_model = joblib.load('fertilizer_model.joblib')
        
        # Model loaded successfully
        
        # Map crop names to match fertilizer dataset
        crop_mapping = {
            'rice': 'Paddy', 'maize': 'Maize', 'chickpea': 'Pulses', 'kidneybeans': 'Pulses',
            'pigeonpeas': 'Pulses', 'mothbeans': 'Pulses', 'mungbean': 'Pulses', 'blackgram': 'Pulses',
            'lentil': 'Pulses', 'pomegranate': 'Fruits', 'banana': 'Fruits', 'mango': 'Fruits',
            'grapes': 'Fruits', 'watermelon': 'Fruits', 'muskmelon': 'Fruits', 'apple': 'Fruits',
            'orange': 'Fruits', 'papaya': 'Fruits', 'coconut': 'Oil seeds', 'cotton': 'Cotton',
            'jute': 'Fiber', 'coffee': 'Beverages'
        }
        
        # Get the mapped crop type, default to 'Maize' if not found
        crop_type = crop_mapping.get(crop_name.lower(), 'Maize')
        
        # Extract features for fertilizer prediction
        # Note: fertilizer model expects: [Temperature, Humidity, Moisture, Soil Type, Crop Type, Nitrogen, Potassium, Phosphorous]
        # We'll use ph as moisture proxy and map soil type
        temperature = soil_features[3]  # temperature from input
        humidity = soil_features[4]     # humidity from input (relative humidity)
        moisture = soil_features[5]     # Using pH as moisture proxy (scaled)
        nitrogen = soil_features[0]     # N from input
        potassium = soil_features[2]    # K from input
        phosphorous = soil_features[1]  # P from input
        
        # Values are now properly mapped for fertilizer prediction
        
        # Create input array for fertilizer prediction
        # Format: [Temperature, Humidity, Moisture, Soil Type, Crop Type, Nitrogen, Potassium, Phosphorous]
        fertilizer_input = [
            temperature,
            humidity,
            moisture,
            soil_type,
            crop_type,
            nitrogen,
            potassium,
            phosphorous
        ]
        
        # Convert to DataFrame with proper column names (exactly as the model expects)
        fertilizer_df = pd.DataFrame([fertilizer_input], columns=[
            'Temparature', 'Humidity', 'Moisture', 'Soil Type', 'Crop Type', 
            'Nitrogen', 'Potassium', 'Phosphorous'
        ])
        
        # DataFrame is now properly formatted for the model
        
        # Make prediction
        predicted_fertilizer = fertilizer_model.predict(fertilizer_df)[0]
        
        return predicted_fertilizer, None
        
    except FileNotFoundError:
        return None, "Error: Fertilizer model file 'fertilizer_model.joblib' not found."
    except KeyError as e:
        return None, f"Error predicting fertilizer: Column mismatch - {e}. Expected columns: Temparature, Humidity, Moisture, Soil Type, Crop Type, Nitrogen, Potassium, Phosphorous"
    except Exception as e:
        return None, f"Error predicting fertilizer: {e}"

# --- 4. Main Application Logic ---
def run_prediction_workflow(user_values):
    """
    Main function to load the model, get user input, and provide recommendations.
    """
    # Load the local crop recommendation model.

    local_prediction = ""
    gemini_info = ""
    fertilizer_prediction = ""
    error = ""

    model_filename = 'crop_model.joblib'
    try:
        model = joblib.load(model_filename)
    except FileNotFoundError:
        error = f"Error: Model file '{model_filename}' not found."
        return local_prediction, gemini_info, fertilizer_prediction, error

    # Initialize the rate limiter: 50 requests per hour (3600 seconds).
    limiter = RateLimiter(max_requests=50, period_seconds=3600)

    try:
        feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        # user_values = [float(input(f"{name.capitalize()}: ")) for name in feature_names]
        
        input_df = pd.DataFrame([user_values], columns=feature_names)
        
        # --- Local Model Prediction ---
        local_prediction = model.predict(input_df)[0].capitalize()

        # --- Fertilizer Prediction ---
        fertilizer_prediction, fertilizer_error = predict_fertilizer(local_prediction, user_values)
        if fertilizer_error:
            error = fertilizer_error

        # --- Gemini API Enrichment (with Rate Limiting) ---
        if limiter.is_allowed():
            gemini_info = get_gemini_details(local_prediction,user_values)
        else:
            gemini_info = "Rate limit of 50 requests per hour exceeded. Please try again later."

    except ValueError:
        error = "Error: Invalid input. Please enter numerical values only."
    except Exception as e:
        error = "An unexpected error occurred: {e}"
    return local_prediction, gemini_info, fertilizer_prediction, error

# --- Execution ---
if __name__ == "__main__":
    run_prediction_workflow()
