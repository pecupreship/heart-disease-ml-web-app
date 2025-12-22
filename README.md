# Heart Disease Prediction Web Application

## Overview
A machine learning–powered web application that predicts the likelihood of heart disease based on patient health metrics. 
Built with Python and Flask, the system loads a trained ML model and provides real-time predictions via a simple web interface.

## Features
- Trained machine learning model (Scikit-learn)
- Flask REST/web application
- HTML frontend for user input
- Real-time prediction results
- Ready for cloud deployment (Render)

## Tech Stack
- Python
- Flask
- Scikit-learn
- Pandas, NumPy
- HTML/CSS

## How It Works
1. User inputs health parameters (age, cholesterol, BP, etc.)
2. Flask backend processes the input
3. Pre-trained ML model (`hd_model.pkl`) generates prediction
4. Result is displayed instantly on the web interface

## Installation
```bash
git clone https://github.com/pecupreship/heart-disease-ml-web-app
cd heart-disease-ml-web-app
pip install -r requirements.txt
python app.py
