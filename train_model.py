import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import warnings

# Suppress unnecessary warnings.
warnings.filterwarnings('ignore')

print("Starting model training process...")

# --- 1. Data Loading and Preparation ---
try:
    df = pd.read_csv('Crop_recommendation.csv')
except FileNotFoundError:
    print("Error: 'Crop_recommendation.csv' not found. Ensure it is in the same directory.")
    exit()

# Define feature and target variables.
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# Split data into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 2. Model Training and Evaluation ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
print("Training the RandomForestClassifier...")
model.fit(X_train, y_train)

# Evaluate the model to confirm performance.
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model trained. Test Accuracy: {accuracy * 100:.2f}%")

# --- 3. Save the Trained Model ---
# This is the crucial step. We use joblib to serialize the model object.
model_filename = 'crop_model.joblib'
joblib.dump(model, model_filename)
print(f"Model saved successfully as '{model_filename}'.")