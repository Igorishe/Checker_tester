FROM python:3.8.5

WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code

CMD python3 Proxy_bot.py