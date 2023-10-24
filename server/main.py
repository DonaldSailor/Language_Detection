from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel
import json
import logging

from transformers import pipeline


class RequestItemSingleText(BaseModel):
    text: str

class RequestItem(BaseModel):
    texts: list

models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    with open('config.json', 'r') as f:
        configuration = json.load(f)
    print('Loading model...')   
    models['language_detector'] = pipeline(model=configuration["model_name"])
    print('Language Model loaded')
    yield
    models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/detect")
async def detect_language_single_text(item: RequestItemSingleText):
    response = {}
    response['language'] = models['language_detector'](item.text)[0]['label']

    return response


@app.post("/detect_batch")
async def detect_language(item: RequestItem):
    texts = item.texts
    response = {}
    scores =  models['language_detector'](texts)
    response['language'] = [i['label'] for i in scores]

    return response