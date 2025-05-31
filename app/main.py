from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predict import make_predictions_alzheimer
from schemas import AlzheimerPredictionResponse

app = FastAPI(title="Alzheimer Detection Image API")

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Autorise le frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            message="Prediction successful"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))