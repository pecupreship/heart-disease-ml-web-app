from flask import Flask, render_template, request, redirect, session
import pandas as pd
import numpy as np
import pickle
from xgboost import XGBClassifier

app = Flask(__name__)

# NEW
app.secret_key = "heart_secret_key"


# Load existing model (if it exists)
try:
    with open('hd_model.pkl', 'rb') as f:
        model = pickle.load(f)
except:
    model = None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    try:

        features = [

            int(request.form['age']),
            int(request.form['sex']),
            int(request.form['cp']),
            float(request.form['trestbps']),
            float(request.form['chol']),
            int(request.form['fbs']),
            int(request.form['restecg']),
            float(request.form['thalach']),
            int(request.form['exang']),
            float(request.form['oldpeak']),
            int(request.form['slope']),
            int(request.form['ca']),
            int(request.form['thal'])

        ]

        prediction = model.predict([np.array(features)])

        result = (
            'Heart Disease Detected 💔'
            if prediction[0] == 1
            else 'No Heart Disease 💖'
        )

        return render_template(
            'index.html',
            prediction_text=result
        )

    except Exception as e:

        return render_template(
            'index.html',
            prediction_text=f'Error: {e}'
        )


# =========================
# NEW LOGIN SYSTEM
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # CHANGE THESE
        if username == 'admin' and password == '1234':

            session['user'] = username

            return redirect('/admin')

    return render_template('login.html')


# =========================
# NEW ADMIN PAGE
# =========================

@app.route('/admin')
def admin():

    # PROTECT PAGE
    if 'user' not in session:
        return redirect('/login')

    return render_template('admin.html')


# =========================
# EXISTING ADD DATA ROUTE
# NOW PROTECTED
# =========================

@app.route('/add-data', methods=['POST'])
def add_data():

    # NEW SECURITY
    if 'user' not in session:
        return redirect('/login')

    try:

        values = [

            int(request.form['age']),
            int(request.form['sex']),
            int(request.form['cp']),
            float(request.form['trestbps']),
            float(request.form['chol']),
            int(request.form['fbs']),
            int(request.form['restecg']),
            float(request.form['thalach']),
            int(request.form['exang']),
            float(request.form['oldpeak']),
            int(request.form['slope']),
            int(request.form['ca']),
            int(request.form['thal']),
            int(request.form['target'])

        ]

        row = pd.DataFrame(
            [values],
            columns=[

                'age',
                'sex',
                'cp',
                'trestbps',
                'chol',
                'fbs',
                'restecg',
                'thalach',
                'exang',
                'oldpeak',
                'slope',
                'ca',
                'thal',
                'target'

            ]
        )

        row.to_csv(
            'heart.csv',
            mode='a',
            header=False,
            index=False
        )

        # Retrain model
        retrain_model()

        return render_template(
            'admin.html',
            prediction_text='✅ New data added and model retrained.'
        )

    except Exception as e:

        return render_template(
            'admin.html',
            prediction_text=f'❌ Error adding data: {e}'
        )


# =========================
# RETRAIN MODEL
# =========================

def retrain_model():

    global model

    hd = pd.read_csv('heart.csv')

    X = hd.drop('target', axis=1)

    Y = hd['target']

    model = XGBClassifier(

        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric='mlogloss',
        subsample=1.0

    )

    model.fit(X, Y)

    with open('hd_model.pkl', 'wb') as f:
        pickle.dump(model, f)


# =========================
# NEW LOGOUT
# =========================

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
