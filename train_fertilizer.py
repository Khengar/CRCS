import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib

# Load data
data = pd.read_csv("Fertilizer Prediction.csv")

# Clean column names
data.columns = data.columns.str.strip()

# Features and target
X = data.drop("Fertilizer Name", axis=1)
y = data["Fertilizer Name"]

# Separate categorical and numeric columns
cat_cols = ["Soil Type", "Crop Type"]
num_cols = ["Temparature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous"]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(), cat_cols)
    ]
)

# Model pipeline
clf = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(random_state=42))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf.fit(X_train, y_train)

# Save the trained model
joblib.dump(clf, "fertilizer_model.joblib")

print("Model trained and saved as fertilizer_model.joblib")