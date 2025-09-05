const axios = require('axios');

async function testWebInterface() {
    console.log('🧪 Testing Web Interface Integration...');
    
    // Test data that matches the form fields
    const testData = {
        N: 50,
        P: 40,
        K: 30,
        temperature: 25,
        humidity: 60,
        ph: 6.5,
        rainfall: 100
    };
    
    try {
        console.log('📤 Sending test data to Flask API...');
        console.log('Test data:', testData);
        
        // Test the Flask API directly
        const response = await axios.post('http://localhost:5000/sendCrop', testData);
        
        console.log('✅ Flask API Response:');
        console.log('   Status:', response.status);
        console.log('   Crop:', response.data.Crop);
        console.log('   Fertilizer:', response.data.Fertilizer);
        console.log('   Gemini Info:', response.data.Gemini ? response.data.Gemini.substring(0, 100) + '...' : 'None');
        console.log('   Error:', response.data.Error || 'None');
        
        console.log('\n🎯 Test completed successfully!');
        console.log('The web interface should now display both crop and fertilizer recommendations.');
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
        if (error.response) {
            console.error('Response status:', error.response.status);
            console.error('Response data:', error.response.data);
        }
        console.log('\n💡 Make sure:');
        console.log('   1. Flask server is running on port 5000');
        console.log('   2. Both crop_model.joblib and fertilizer_model.joblib exist');
        console.log('   3. All dependencies are installed');
    }
}

// Run the test
testWebInterface();
