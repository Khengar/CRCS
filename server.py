from flask import Flask
from flask import request
import json
from PredictCrop import run_prediction_workflow

app = Flask(__name__)

@app.route("/sendCrop", methods=["GET", "POST"])
def sendCrop():
    if request.method == "POST":
        data = request.json.values() #Converting Json to dictionary further to list
        data = list(map(float, data)) #Converting every member of list's datatype to float
        crop, geminiInfo, error = run_prediction_workflow(data)
        return {"Crop": crop, "Gemini": geminiInfo, "Error": error}
    else:
        return "Invalid request method"
