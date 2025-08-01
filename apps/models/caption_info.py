from pydantic import BaseModel

class CaptionBase64Req(BaseModel):
    base64str: str