from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predict import make_predictions_alzheimer
from schemas import AlzheimerPredictionResponse

app = FastAPI(title="Alzheimer Detection Image API")

# Add CORS middleware to allow requests from Ngrok
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Image-based prediction API is running!"}

@app.post("/predict", response_model=AlzheimerPredictionResponse)
async def predict(file: UploadFile = File(...)):
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Processing file: {file.filename}")
        prediction = make_predictions_alzheimer(file)
        logger.info(f"Prediction result: {prediction}")
        if prediction is None:
            raise ValueError("Prediction returned None")
        return AlzheimerPredictionResponse(
            filename=file.filename,
            prediction=prediction,
            message="Prediction successful"
        )
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))