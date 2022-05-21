from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import redis

from question_generation.pipelines import pipeline

# init app
app = FastAPI()
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_passkey = os.getenv('REDIS_PASSKEY')
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_passkey, decode_responses=True)
# add cors origins rules 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
             
nlp = pipeline("e2e-qg")

class Payload(BaseModel):
    query: str


@app.post("/")
def main( payload: Payload):
    query = payload.query
    print('Question asked: ', query)
    if r.sismember('context:', query) is False:
        print('caching to be done')
        questions=nlp(query)
        r.hset('rastero:e2eqg:'+query, query, questions[0])
        r.sadd('rastero:e2eqg:', query)
        return questions[0]
        
    else: 
        print('file available in redis cache! 😇')
        response = r.hget('rastero:e2eqg:'+query, query)
        return response


@app.get("/")
async def root():
    return {"message": "e2eqg"}