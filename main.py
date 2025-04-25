from fastapi import FastAPI
from apps.router import (fileanalysis)
from fastapi.middleware.cors import CORSMiddleware


import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

app = FastAPI()

# 允许所有来源的跨域请求
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    # 允许的来源列表
    allow_origins=origins,
    # 允许携带凭证（如 cookies）
    allow_credentials=True,
    # 允许的 HTTP 请求方法
    allow_methods=["*"],
    # 允许的 HTTP 请求头
    allow_headers=["*"],
)

app.include_router(fileanalysis.router, prefix="/api/v1/file", tags=["fileanalysis"])

