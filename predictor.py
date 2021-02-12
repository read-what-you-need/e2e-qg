# download and upload files to s3

import os, subprocess
import io

import redis



from question_generation.pipelines import pipeline

class PythonPredictor:

    def __init__(self, config):
      self.nlp = pipeline("e2e-qg")

      self.redis_host = os.getenv('REDIS_HOST')
      self.redis_port = os.getenv('REDIS_PORT')
      self.redis_passkey = os.getenv('REDIS_PASSKEY')

      self.r = redis.StrictRedis(host=self.redis_host, port=self.redis_port, password=self.redis_passkey, ecode_responses=True)



        
    def predict(self, payload):
      
      text=payload['text']
      
      if self.r.sismember('context:', text) is False:
        print('caching to be done')
        
        questions=self.nlp(text)
        
        self.r.hset('context:'+text, text, questions[0])
        self.r.sadd('context:', text)

        return questions[0]

        

      else:

        print('file available in redis cache! 😇')
        response = self.r.hget('context:'+text, text)

        return response
      
	
        



