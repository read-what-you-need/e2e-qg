from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from question_generation.pipelines import pipeline

# init app
app = FastAPI()

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
  questions=nlp(query)
  return questions