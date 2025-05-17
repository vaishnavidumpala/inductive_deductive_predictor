# Inductive and Deductive Learning Style Predictor

A web-based intelligent system to identify whether a student is an **inductive** or **deductive** learner, enabling personalized learning strategy recommendations based on quiz responses and machine learning prediction.

---

## 👨‍💻 Project Overview

This project aims to support students in identifying their learning preferences using a dynamic web application. It features:

- A quiz interface that collects student responses to 14 behavior-based questions.
- A machine learning model that predicts the user's learning style (Inductive/Deductive).
- A result page that displays the prediction along with tailored study material suggestions.
- A user-friendly interface with authentication (login/signup).
- Backend built with **Node.js (Express)** and **Python (Flask)** for ML inference.
- ML models trained on a custom dataset using **Scikit-learn**.

---

## 💡 Features

- ✅ User authentication system (Signup/Login)
- ✅ Swiper.js-based animated quiz interface (14 questions)
- ✅ Real-time ML prediction using a Flask API
- ✅ Recommendations on learning materials
- ✅ Responsive and accessible UI with particle effects and modern styling
- ✅ Administered using Node.js and MongoDB

---

## 🔧 Technologies Used

### 🌐 Frontend
- HTML5, CSS3, JavaScript, EJS
- Swiper.js – for quiz carousel
- Particles.js – for animated background

### ⚙ Backend
- **Express.js** (Node.js) – web server
- **Flask** (Python) – ML prediction API
- **bcrypt** – password hashing
- **axios** – HTTP client to communicate with Flask
- **MongoDB** + **Mongoose** – database and ODM

### 🤖 Machine Learning
- **Flask** – ML API
- **scikit-learn** – ML models (Random Forest, SVM, etc.)
- **imbalanced-learn** – SMOTE for class balancing
- **pandas**, **numpy** – data handling
- **pickle** – saving trained models and preprocessors

---

## 📁 Project Directory Structure

inductive_deductive/
├── backend/
│ ├── app.py
│ ├── model.pkl
│ ├── preprocessor.pkl
│ ├── encoder.pkl
│ └── preprocessing.py
│
├── dataset/
│ └── inductive_deductive_data.csv
│
├── public/
│
├── src/
│ ├── index.js
│ └── config.js
│
├── views/
│ ├── signup.ejs
│ ├── login.ejs
│ ├── info.ejs
│ ├── home.ejs
│ └── result.ejs
│
├── package.json
└── README.md

---

## 🏁 How to Run Locally

> Ensure MongoDB is running locally before starting the project.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/inductive-deductive-predictor.git
cd inductive-deductive-predictor

### 2️⃣ Setup Node.js Backend

cd src
npm install express ejs bcrypt mongoose axios
node index.js

### 3️⃣ Setup Flask ML Backend

cd ../backend
pip install flask flask-cors scikit-learn pandas numpy imbalanced-learn
python app.py

### 4️⃣ Run the App

Open your browser and navigate to: http://localhost:5001
Register or log in to access the quiz.
After completing the quiz, you’ll see your predicted learning style with tailored resources.


