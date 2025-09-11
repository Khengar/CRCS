#!/usr/bin/env python3
"""
Test script for the enhanced Crop and Fertilizer Prediction API
"""

import requests
import json

def test_prediction_api():
    """Test the prediction API endpoint"""
    
    # Test data: [N, P, K, temperature, humidity, ph, rainfall]
    test_data = {
        "N": 50,
        "P": 40, 
        "K": 30,
        "temperature": 25,
        "humidity": 60,
        "ph": 6.5,
        "rainfall": 100
    }
    
    # API endpoint
    url = "http://localhost:5000/sendCrop"
    
    try:
        print("Testing Crop and Fertilizer Prediction API...")
        print(f"Input data: {test_data}")
        print("-" * 50)
        
        # Make POST request
        response = requests.post(url, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response:")
            print(f"   Crop: {result.get('Crop', 'N/A')}")
            print(f"   Fertilizer: {result.get('Fertilizer', 'N/A')}")
            print(f"   Gemini Info: {result.get('Gemini', 'N/A')[:100]}...")
            print(f"   Error: {result.get('Error', 'None')}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the server is running on localhost:5000")
    except Exception as e:
        print(f"❌ Test Error: {e}")

def test_health_check():
    """Test the health check endpoint"""
    
    url = "http://localhost:5000/health"
    
    try:
        print("\nTesting Health Check...")
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health Check: {result}")
        else:
            print(f"❌ Health Check Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the server is running on localhost:5000")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")

if __name__ == "__main__":
    print("🚀 Crop and Fertilizer Prediction API Test")
    print("=" * 50)
    
    # Test health check first
    test_health_check()
    
    # Test prediction API
    test_prediction_api()
    
    print("\n" + "=" * 50)
    print("Test completed!")
