from pydantic import BaseModel, Field

class FrameEvent(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    frame_base64: str = Field(min_length=10)
    timestamp: float

class AlertEvent(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    signal: str = Field(min_length=1, max_length=50)
    severity: int = Field(default=1, ge=0, le=5)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    message: str = Field(default="")
    timestamp: float = 0.0
