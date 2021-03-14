import pickle5 as pickle
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
import boto3
import boto3.session

def text_cleaner(news):
    nopunc = [char for char in news if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

def predict(inputs):
    s3client = boto3.client('s3')
    response = s3client.get_object(Bucket='bucket_name', Key='model_nb-2.sav')
    body = response['Body'].read()
    model_1 = pickle.loads(body)
    news_test=pd.Series(data=[inputs])
    val = model_1.predict(news_test)
    return val