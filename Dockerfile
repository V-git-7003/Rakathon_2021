FROM python:3.8

WORKDIR /Hackathon_2021

RUN pip install scrapy

RUN pip install boto3

COPY / .

CMD [ "python", "./src/bankingcrawler.py" ]