from fastapi.routing import APIRouter
from fastapi import UploadFile, File
import shutil
from app.core.utils.yolov8s import detect_objects
from app.api.models import DetectionResponse
import os

app=APIRouter(prefix="/object",tags=["object"])


@app.post("/detect")
async def detect_object(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    img_byte_arr, detected_objects = detect_objects(file.filename)
    os.remove(file.filename)  # Delete the input image after processing
    return DetectionResponse(detected_objects=detected_objects, processed_image=img_byte_arr)