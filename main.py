from fastapi import FastAPI
from apps.router import (fileanalysis)


import nltk
nltk.download('punkt_tab')

app = FastAPI()

app.include_router(fileanalysis.router, prefix="/api/v1/file", tags=["fileanalysis"])

