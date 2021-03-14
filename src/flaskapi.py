from flask import Flask, json,request,jsonify,make_response
import pickle5 as pickle
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
import boto3
import boto3.session
import prediction

def text_cleaner(news):
    nopunc = [char for char in news if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]



api = Flask(__name__)

@api.route('/prediction', methods=['POST'])
def get_prediction():
  try:
    input = request.get_json()
    user_input = input['input']
    if(user_input != None):
      value = prediction.predict(user_input) 
      values = []
      for i in value:
          if i == 1 :
            values.append("positive news")
          else :
            values.append("negative news")
      message = "success"
      code = 200
    else:
      values = None
      message = "bad request."
      code = 404
  except:
    values = None
    message = "Some thing went wrong."
    code = 404

  response = make_response(
    jsonify(
        {"value": str(values), "message": message}
    ),
    code,
  )
  response.headers["Content-Type"] = "application/json"

  return response

if __name__ == '__main__':
    api.run()