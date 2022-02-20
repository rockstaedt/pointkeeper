FROM python:3.9-slim

MAINTAINER Eric Rockstädt <rockstaedt@rackow-berlin.de>

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app

WORKDIR /app

CMD ["flask", "run", "-h", "0.0.0.0"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
