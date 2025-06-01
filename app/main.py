from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predict import make_predictions_alzheimer
from schemas import AlzheimerPredictionResponse
import mlflow
from mlflow.tracking import MlflowClient

app = FastAPI(title="Alzheimer Detection Image API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mlflow.set_tracking_uri("http://mlflow_ui:5000")
client = MlflowClient()

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
        predicted_class, confidence = make_predictions_alzheimer(file)
        logger.info(f"Prediction result: {predicted_class}, Confidence: {confidence}")
        if predicted_class is None:
            raise ValueError("Prediction returned None")
        return AlzheimerPredictionResponse(
            filename=file.filename,
            prediction=predicted_class,
            message=f"Prediction successful",
            confidence=confidence
        )
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
async def get_logs(limit: int = 10):
    try:
        runs = client.search_runs(experiment_ids=["0"], max_results=limit, order_by=["start_time DESC"])
        logs = []
        for run in runs:
            log = {
                "run_id": run.info.run_id,
                "filename": run.data.params.get("image_filename", "N/A"),
                "predicted_class": int(run.data.metrics.get("predicted_class", -1)),
                "confidence": run.data.metrics.get("prediction_confidence", 0.0),
                "latency": run.data.metrics.get("prediction_latency", 0.0),
                "timestamp": run.info.start_time.isoformat()
            }
            logs.append(log)
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching logs: {str(e)}")