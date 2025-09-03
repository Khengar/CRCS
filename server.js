import express from "express";
import { dirname } from "path";
import { fileURLToPath } from "url";
import axios from "axios";

const __dirname__ = dirname(fileURLToPath(import.meta.url));

const app = express();

app.use(express.urlencoded({extended:true}));

app.use('/static', express.static(__dirname__ + "//web//static"));

app.listen(2000, ()=>{console.log("Server running at port: 2000")});

app.get("/", (req,res)=>{
    res.render(__dirname__ + '//web//index.ejs', {
        crop: null,
        fertilizer: null,
        cropContent: null,
        inputData: null
    });
})

app.post("/", async (req,res)=>{
    try {
        // Validate required fields
        const requiredFields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'];
        const missingFields = requiredFields.filter(field => !req.body[field]);
        
        if (missingFields.length > 0) {
            return res.render(__dirname__ + "//web//index.ejs", {
                crop: null,
                fertilizer: null,
                cropContent: `Missing required fields: ${missingFields.join(', ')}`,
                inputData: req.body
            });
        }
        
        const response = await axios.post("http://localhost:5000/sendCrop", req.body);
        const {Crop, Fertilizer, Gemini, Error} = response.data;
        
        if (Error) {
            res.render(__dirname__ + "//web//index.ejs",  {
                crop: null,
                fertilizer: null,
                cropContent: `Error: ${Error}`,
                inputData: req.body
            });
        } else {
            res.render(__dirname__ + "//web//index.ejs",  {
                crop: Crop,
                fertilizer: Fertilizer,
                cropContent: Gemini || 'No AI analysis available',
                inputData: req.body // Send back data to show what was entered
            });
        }
    } catch (error) {
        console.error("Error calling prediction API:", error);
        let errorMessage = 'Server Error: Unable to connect to prediction service';
        
        if (error.code === 'ECONNREFUSED') {
            errorMessage = 'Error: Prediction service is not running. Please start the Flask server first.';
        } else if (error.response) {
            errorMessage = `API Error: ${error.response.status} - ${error.response.statusText}`;
        } else if (error.message) {
            errorMessage = `Error: ${error.message}`;
        }
        
        res.render(__dirname__ + "//web//index.ejs",  {
            crop: null,
            fertilizer: null,
            cropContent: errorMessage,
            inputData: req.body
        });
    }
})