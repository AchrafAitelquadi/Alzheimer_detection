from fastapi import FastAPI, UploadFile, File, HTTPException
from app.predict import make_predictions_alzheimer
from app.schemas import AlzheimerPredictionResponse

app = FastAPI(title="Alzheimer Detection Image API")

@app.get("/")
def root():
    return {"message": "Image-based prediction API is running!"}

@app.post("/predict", response_model=AlzheimerPredictionResponse)
async def predict(file: UploadFile = File(...)):
    try:
        prediction = make_predictions_alzheimer(file)
        return AlzheimerPredictionResponse(
            filename=file.filename,
            prediction=prediction,
            message="Prediction succesfull"
        )
    except Exception as e:
        raise HTTPException(status_code= 500, detail= str(e))