FROM python:3.8-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install psycopg2-binary

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "tt-main.py" ]