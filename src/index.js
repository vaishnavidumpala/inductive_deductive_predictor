const express = require('express');
const path = require('path');
const bcrypt = require('bcrypt');
const collection = require('./config');
const axios = require('axios');

// Create an express application
const app = express();

// Middleware to parse JSON and URL-encoded data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));



// Set the views directory
app.set('views', path.join(__dirname, '..', 'views'));  // Update path as per your folder structure

// Use EJS as the view engine
app.set('view engine', 'ejs');

// Serve static files (e.g., images, CSS, JS)
app.use(express.static("public"));

// Render login page (GET request)
app.get("/", (req, res) => {
    res.render("login");
});

app.get("/login",(req,res)=>{
    res.render("login")
})

// Render signup page (GET request)
app.get("/signup", (req, res) => {
    res.render("signup");
});

app.get("/home", (req, res) => {
    res.render("home");
});


// Render info page after login/signup (GET request)
app.get("/info", (req, res) => {
    res.render("info");
});

// Render result page based on prediction results (GET request)
app.get('/result', (req, res) => {
    const inductive_percentage = parseFloat(req.query.inductive_percentage) || 0;
    const deductive_percentage = parseFloat(req.query.deductive_percentage) || 0;
  
    res.render('result', {
      prediction: req.query.prediction,
      inductive_percentage: inductive_percentage,
      deductive_percentage: deductive_percentage
    });
});
  

// Register user (POST request)
app.post("/signup", async (req, res) => {
    const data = {
        name: req.body.username,
        password: req.body.password
    };

    try {
        // Check if the user already exists
        const existingUser = await collection.findOne({ name: data.name });
        if (existingUser) {
            return res.send("Username already exists");
        }

        // Hash the password
        const saltRounds = 10;
        const hashedPassword = await bcrypt.hash(data.password, saltRounds);
        data.password = hashedPassword;

        const result = await collection.insertOne(data);
        // Redirect to login page after successful signup
        res.redirect('/');
    } catch (err) {
        console.error(err);
        res.send("Error registering user.");
    }
});

// Login user (POST request)
app.post("/login", async (req, res) => {
    try {
        const user = await collection.findOne({ name: req.body.username });
        if (!user) {
            return res.render("login", { error: "Username not found" });
        }

        const isPasswordMatch = await bcrypt.compare(req.body.password, user.password);
        if (isPasswordMatch) {
            // Redirect to info page after successful login
            res.redirect('/info');
        } else {
            res.render("login", { error: "Wrong password" });
        }
    } catch (err) {
        console.error(err);
        res.render("login", { error: "Error occurred during login." });
    }
});

// Predict and process answers (POST request)
app.post('/predict',  async (req, res) => {
    const answers = req.body;

    try {
        // Send answers to the Flask backend for prediction
        const response = await axios.post('http://127.0.0.1:5000/predict', answers);

        const { prediction, inductive_percentage, deductive_percentage } = response.data;

        // Send the prediction response back to the client
        res.json({ prediction, inductive_percentage, deductive_percentage });
    } catch (error) {
        res.status(500).json({ error: 'Prediction failed. Please try again later.' });
    }
});
// Logout route to clear token (if needed)
app.get('/logout', (req, res) => {
    res.redirect('/')
});

// Start the server on port 5001
const port = 5001;
app.listen(port, () => {
    console.log(`Server running on Port: ${port}`);
});
