from fastapi import APIRouter
from schemas import PredictRequest, PredictResponse
from ml.predictor import predict_transaction

router = APIRouter()

@router.post('/', response_model=PredictResponse)
def predict(req: PredictRequest):
    result = predict_transaction(req.dict())
    return result
