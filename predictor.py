# download and upload files to s3

import os, subprocess
import io

from question_generation.pipelines import pipeline

class PythonPredictor:

    def __init__(self, config):
      self.nlp = pipeline("e2e-qg")


        
    def predict(self, payload):
      
      text=payload['text']
      
        
      questions=self.nlp(text)
        
      response = questions[0]

      return response
