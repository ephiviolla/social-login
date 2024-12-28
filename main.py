import logging.config
import os

import yaml
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from backend.app.config.config import LoadSetting
from backend.app.routers.naver_router import router as naver_router
from backend.app.utils.logging_util import LoggingUtil

settings = LoadSetting()()

origins = [
    'http://localhost',
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 정적 파일 설정
app.mount('/frontend/index.html', StaticFiles(directory='frontend'), name='frontend')

# 라우터 연결
app.include_router(router=naver_router, tags=['social'])

# 로그 설정
LOG_DIR = os.getenv('LOG_DIR', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'sqlalchemy_queries.log')
os.makedirs(LOG_DIR, exist_ok=True)

# 로그 설정 파일 적용
with open('logging.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)
LoggingUtil(name='fastapi')


@app.get('/')
async def root():
    return FileResponse('frontend/index.html')
