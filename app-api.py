from fastapi import APIRouter, UploadFile
from .models import InputSchema, BatchInput
from .services import run_single, run_batch
from .utils import load_csv

router = APIRouter()


@router.post("/predict")
def predict(data: InputSchema):
    return run_single(data.dict())


@router.post("/batch")
def batch(data: BatchInput):
    return run_batch([r.dict() for r in data.records])


@router.post("/upload-csv")
async def upload_csv(file: UploadFile):
    records = load_csv(file.file)
    return run_batch(records)