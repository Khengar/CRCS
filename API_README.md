# Enhanced Crop and Fertilizer Prediction API

This API now provides both crop recommendations and fertilizer suggestions based on soil and climate conditions.

## Features

- **Crop Prediction**: Recommends the best crop based on soil nutrients and environmental conditions
- **Fertilizer Prediction**: Suggests optimal fertilizer for the predicted crop
- **AI Enrichment**: Uses Google Gemini API to provide detailed explanations
- **Error Handling**: Comprehensive error handling and validation

## API Endpoints

### 1. Prediction Endpoint
**POST** `/sendCrop`

**Input Format:**
```json
{
    "N": 50,           // Nitrogen ratio in soil
    "P": 40,           // Phosphorus ratio in soil  
    "K": 30,           // Potassium ratio in soil
    "temperature": 25,  // Temperature in Celsius
    "humidity": 60,     // Relative humidity percentage
    "ph": 6.5,         // pH value of soil
    "rainfall": 100     // Rainfall in mm
}
```

**Response Format:**
```json
{
    "Crop": "Maize",
    "Fertilizer": "Urea", 
    "Gemini": "Detailed explanation from AI...",
    "Error": null
}
```

### 2. Health Check
**GET** `/health`

Returns API status and health information.

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server:**
   ```bash
   python server.py
   ```

3. **Test the API:**
   ```bash
   python test_server.py
   ```

## How It Works

1. **Input Validation**: Validates that exactly 7 features are provided
2. **Crop Prediction**: Uses the trained crop model to predict suitable crops
3. **Fertilizer Prediction**: Automatically predicts the best fertilizer for the recommended crop
4. **AI Enhancement**: Uses Google Gemini API to provide detailed explanations
5. **Response**: Returns all predictions in a structured JSON format

## Error Handling

- **400 Bad Request**: Invalid input data (wrong number of features)
- **405 Method Not Allowed**: Using GET instead of POST
- **500 Internal Server Error**: Server-side errors during prediction

## Example Usage

### Python
```python
import requests

data = {
    "N": 50, "P": 40, "K": 30,
    "temperature": 25, "humidity": 60,
    "ph": 6.5, "rainfall": 100
}

response = requests.post("http://localhost:5000/sendCrop", json=data)
result = response.json()

print(f"Recommended Crop: {result['Crop']}")
print(f"Recommended Fertilizer: {result['Fertilizer']}")
print(f"AI Explanation: {result['Gemini']}")
```

### JavaScript/Fetch
```javascript
const data = {
    N: 50, P: 40, K: 30,
    temperature: 25, humidity: 60,
    ph: 6.5, rainfall: 100
};

fetch('http://localhost:5000/sendCrop', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
    console.log('Crop:', result.Crop);
    console.log('Fertilizer:', result.Fertilizer);
    console.log('AI Info:', result.Gemini);
});
```

## Model Files Required

- `crop_model.joblib` - Pre-trained crop prediction model
- `fertilizer_model.joblib` - Pre-trained fertilizer prediction model

## Notes

- The API automatically maps crop names from the crop model to fertilizer dataset categories
- CORS is enabled for cross-origin requests
- Rate limiting is implemented for the Gemini API (50 requests per hour)
- The server runs on `localhost:5000` by default
