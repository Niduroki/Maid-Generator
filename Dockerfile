FROM python:3.7-slim

RUN apt-get update && apt-get install -y gcc && pip install flask uwsgi

RUN mkdir /maid/
WORKDIR /maid/
COPY . /maid/

EXPOSE 80

CMD [ "uwsgi", "maid-py.ini" ]
