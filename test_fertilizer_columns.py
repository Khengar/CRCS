#!/usr/bin/env python3
"""
Test script to debug fertilizer prediction column issues
"""

import joblib
import pandas as pd
import numpy as np

def test_fertilizer_model():
    """Test the fertilizer model to understand its column requirements"""
    
    try:
        print("🔍 Testing Fertilizer Model Column Requirements...")
        print("=" * 60)
        
        # Load the model
        model = joblib.load('fertilizer_model.joblib')
        print("✅ Model loaded successfully")
        
        # Check model attributes
        print(f"\n📊 Model type: {type(model)}")
        
        if hasattr(model, 'feature_names_in_'):
            print(f"✅ Model feature names: {model.feature_names_in_}")
        else:
            print("❌ Model doesn't have feature_names_in_ attribute")
        
        if hasattr(model, 'named_steps'):
            print(f"✅ Model has named steps: {list(model.named_steps.keys())}")
            
            if 'preprocessor' in model.named_steps:
                preprocessor = model.named_steps['preprocessor']
                print(f"✅ Preprocessor type: {type(preprocessor)}")
                
                if hasattr(preprocessor, 'get_feature_names_out'):
                    feature_names = preprocessor.get_feature_names_out()
                    print(f"✅ Preprocessor feature names: {feature_names}")
                else:
                    print("❌ Preprocessor doesn't have get_feature_names_out method")
        else:
            print("❌ Model doesn't have named_steps attribute")
        
        # Test with sample data
        print("\n🧪 Testing with sample data...")
        
        # Create sample data with exact column names from dataset
        sample_data = pd.DataFrame([[
            25,    # Temparature
            60,    # Humidity (with space)
            6.5,   # Moisture (pH as proxy)
            'Loamy', # Soil Type
            'Maize', # Crop Type
            50,    # Nitrogen
            30,    # Potassium
            40     # Phosphorous
        ]], columns=[
            'Temparature', 'Humidity ', 'Moisture', 'Soil Type', 'Crop Type', 
            'Nitrogen', 'Potassium', 'Phosphorous'
        ])
        
        print(f"📋 Sample data columns: {sample_data.columns.tolist()}")
        print(f"📏 Sample data shape: {sample_data.shape}")
        print(f"📊 Sample data:\n{sample_data}")
        
        # Try to make prediction
        try:
            prediction = model.predict(sample_data)
            print(f"✅ Prediction successful: {prediction[0]}")
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            print(f"🔍 Error type: {type(e)}")
            
            # Try to understand the error better
            if 'columns are missing' in str(e):
                print("🔍 This is a column mismatch error")
                # Extract missing columns from error message
                import re
                missing_match = re.search(r"columns are missing: \{'([^']+)'\}", str(e))
                if missing_match:
                    missing_col = missing_match.group(1)
                    print(f"🔍 Missing column: '{missing_col}'")
                    print(f"🔍 Available columns: {sample_data.columns.tolist()}")
                    
                    # Check for exact match
                    for col in sample_data.columns:
                        if col == missing_col:
                            print(f"✅ Column '{col}' exists exactly")
                        elif col.strip() == missing_col:
                            print(f"⚠️ Column '{col}' exists but with whitespace differences")
                        else:
                            print(f"❌ Column '{col}' doesn't match '{missing_col}'")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")

if __name__ == "__main__":
    test_fertilizer_model()
