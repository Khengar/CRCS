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
    res.render(__dirname__ + '//web//index.ejs');
})

app.post("/", async (req,res)=>{
    const response = await axios.post("http://localhost:5000/sendCrop", req.body);
    const {Crop,Gemini} = response.data;
    res.render(__dirname__ + "//web//index.ejs",  {
        crop: Crop,
        cropContent: Gemini,
        inputData: req.body // Send back data to show what was entered
    });
})