from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

# Create a FastAPI instance
app = FastAPI()

# Load the trained VAE model
try:
    vae_model = load_model("../../models/vae_model.h5")
except Exception as e:
    print(f"Error loading model: {e}")

# Route for file upload and anomaly detection
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return HTTPException(status_code=400, detail="File type not supported. Please upload a .csv file.")

    try:
        # Read the uploaded CSV file into a pandas DataFrame
        df = pd.read_csv(file.file)
        
        # Check if the dataframe is empty or has incorrect columns
        if df.empty:
            return JSONResponse(status_code=400, content={"detail": "The uploaded CSV file is empty."})
        
        # Normalize the data using StandardScaler
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df)
        
        # Pass the data through the VAE model
        reconstructed_data = vae_model.predict(scaled_data)
        
        # Calculate the reconstruction error
        error = np.mean(np.square(scaled_data - reconstructed_data), axis=1)
        
        # Set a threshold for anomalies (you may need to tune this)
        threshold = 0.1
        
        # Identify anomalies
        anomalies = error > threshold
        anomaly_count = np.sum(anomalies)
        total_count = len(anomalies)
        
        # Return results
        return {
            "anomalies_detected": int(anomaly_count),
            "total_records": total_count,
            "anomaly_percentage": round((anomaly_count / total_count) * 100, 2)
        }

    except Exception as e:
        # Return an error response in case of an exception
        return HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

# To run FastAPI, use the following command:
# uvicorn app:app --reload
