from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from PredictCrop import run_prediction_workflow

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route("/sendCrop", methods=["GET", "POST"])
def sendCrop():
    if request.method == "POST":
        try:
            # Get JSON data from request
            data = request.json.values() #Converting Json to dictionary further to list
            data = list(map(float, data)) #Converting every member of list's datatype to float
            
            # Validate input data length (should be 7 features: N, P, K, temperature, humidity, ph, rainfall)
            if len(data) != 7:
                return jsonify({
                    "Error": "Invalid input: Expected 7 features (N, P, K, temperature, humidity, ph, rainfall)",
                    "Crop": None,
                    "Gemini": None,
                    "Fertilizer": None
                }), 400
            
            # Run prediction workflow
            crop, geminiInfo, fertilizer, error = run_prediction_workflow(data)
            
            # Return results
            return jsonify({
                "Crop": crop,
                "Gemini": geminiInfo,
                "Fertilizer": fertilizer,
                "Error": error
            })
            
        except Exception as e:
            return jsonify({
                "Error": f"Server error: {str(e)}",
                "Crop": None,
                "Gemini": None,
                "Fertilizer": None
            }), 500
    else:
        return jsonify({
            "Error": "Invalid request method. Use POST method.",
            "Crop": None,
            "Gemini": None,
            "Fertilizer": None
        }), 405

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Crop and Fertilizer Prediction API is running"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
