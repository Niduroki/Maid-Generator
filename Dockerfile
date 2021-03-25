FROM python:3-slim

RUN apt-get update && apt-get install -y gcc && pip install flask uwsgi

RUN mkdir /maid/
WORKDIR /maid/
COPY . /maid/
RUN useradd uwsgi && chown -R uwsgi /maid

EXPOSE 8000

USER uwsgi
CMD [ "uwsgi", "maid-py.ini" ]
