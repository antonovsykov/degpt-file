from pydantic import BaseModel
from typing import Optional

class CaptionInfoReq(BaseModel):
    language: Optional[str] = None
    base64str: Optional[str] = None
    fileurl: Optional[str] = None