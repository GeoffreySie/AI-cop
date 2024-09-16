from flask import Flask, request, render_template
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the model and scaler
vae = load_model('../model/vae_model.h5')
scaler = StandardScaler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    df = pd.read_csv(file)

    # Preprocess and predict
    X = scaler.transform(df.drop('attack_type', axis=1))
    X_reconstructed = vae.predict(X)
    reconstruction_error = ((X - X_reconstructed) ** 2).mean(axis=1)

    threshold = 0.01
    anomalies = reconstruction_error > threshold

    df['is_anomaly'] = anomalies
    return df.to_html()

if __name__ == '__main__':
    app.run(debug=True)
