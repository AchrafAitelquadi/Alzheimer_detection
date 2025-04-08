from pydantic import BaseModel

#Defining the API response after prediction
class AlzheimerPredictionResponse(BaseModel):
    filename : str
    prediction : int
    message : str
