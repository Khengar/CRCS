# CRCS
A simple, two-server crop recommendation app that runs a Python API and a JavaScript frontend concurrently, connected over a REST interface and trained on the Crop Recommendation dataset using scikit-learn.

## Overview
- The project consists of two servers that run at the same time: a Python API and a JS frontend, communicating via REST.
- The machine learning model is trained with scikit-learn on Crop_recommendation.csv, and the project includes commands and dependencies to reproduce the setup.
- The repository contains Python, CSS, EJS, and JavaScript files, reflecting a server-rendered JS frontend with EJS templates and a Python backend API.

## Features
- Two-server architecture: Python API + JS frontend with REST communication.
- Model trained using scikit-learn on Crop_recommendation.csv.
- Reproducible environment via requirements.txt for Python and npm install for Node dependencies.

## Prerequisites
- Python and pip installed to run the Flask-based API.
- Node.js and npm installed to run the JS frontend and install dependencies.
- Basic ability to run two terminal sessions to start both servers concurrently.

## Project setup
1. Clone the repository
   - git clone <repo-url> && cd CRCS.
   - `git clone github.com/AnkitSinghGTHB/CRCS`
   - `cd CRCS`
2. Python environment
   - Create and activate a virtual environment (optional but recommended).
      - `python -m venv virt` 
   - Install dependencies:
      - `pip install -r requirements.txt`
3. Node.js dependencies
   - Install frontend deps:
      -  `npm i`

## Running the servers
Open two terminals—one for the Python API and one for the JS frontend.

- Terminal A (Python API) [Backend]
   - Identify the Python app module (a .py file that defines the Flask app), then run using Flask’s CLI: flask --app <python_module_without_py> run.
   - Example: if the entry file is app.py, use: flask --app app run.
   - Note: If previous instructions said flask --app server.js run, change to the correct Python module since Flask requires a Python module, not a .js file.
   - In our project we have used:   `flask --app server.py run`

- Terminal B (JS frontend)
   - Start the frontend: nodemon start server.js (or use node server.js if nodemon isn’t installed globally).
   - We have used `nodemon start server.js`

Once both servers are running, access the frontend in the browser; it will call the API over REST as configured in the JS server code.

## Training the model
- The model is trained using scikit-learn on Crop_recommendation.csv.
- Follow the steps in commands.txt to retrain or reproduce the model locally (for example, fit, evaluate, and persist the model).
- If a serialized model file is used by the API, ensure the API’s load path matches the model’s save location after training.

## Expected inputs
- Typical crop recommendation features include N, P, K (soil nutrients), temperature, humidity, pH, and rainfall; align the API payload with how the Flask route consumes inputs in the codebase.
- Verify the exact request body structure and endpoint path by checking the Flask routes in the API module.

## Development notes
- requirements.txt contains the Python dependencies needed for the API.
- npm i installs the Node dependencies required by the JS frontend with EJS templates and CSS assets.
- Use nodemon for hot reloading of the JS server during development; install globally (npm i -g nodemon) if the nodemon command is unavailable.

## Troubleshooting
- Flask app module: Ensure the --app target is a Python module (e.g., app), not a JavaScript file; the CLI accepts module names and files like app.py (run as flask --app app run).
- Ports: If default ports conflict, update the port in the Flask CLI (flask --app app run --port 5001) or in the JS server configuration before starting both servers.
- Dataset path: Confirm the API and training code reference the correct Crop_recommendation.csv path before running.

## Repository contents
- Python API with scikit-learn model training based on Crop_recommendation.csv.
- JS frontend using EJS templates and CSS, with a server.js entry point.
- requirements.txt and commands.txt for reproducible setup and training instructions.

## License
- No license information is provided in the current fork metadata.

## Acknowledgments
- Crop Recommendation Dataset (Kaggle).
