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

savekey="rastero:e2eqg:"
@app.post("/")
def main( payload: Payload):
    query = payload.query
    print('Question asked: ', query)
    if r.hexists(savekey, query) is False:
        print('caching to be done')
        questions=nlp(query)
        try:
            questions[0]
        except Exception as e:
            print(e)
            return "Question could not be generated."
        else:
            r.hset(savekey, query, questions[0])
            return questions[0]
        
    else: 
        print('file available in redis cache! 😇')
        response = r.hget(savekey, query)
        print('response: ', response) 
        return response


@app.get("/")
async def root():
    return {"message": "e2eqg"}