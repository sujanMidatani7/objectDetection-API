from pydantic import BaseModel

class DetectionResponse(BaseModel):
    detected_objects: dict[str, int]
    processed_image: str