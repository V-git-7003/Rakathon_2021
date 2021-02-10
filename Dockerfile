FROM python:3.8

WORKDIR /hackathon_2021

RUN pip install scrapy

COPY / .

CMD [ "python", "./src/test.py" ]