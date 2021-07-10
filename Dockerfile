FROM python:3-slim

RUN apt-get update && apt-get install -y gcc
ENV VIRTUAL_ENV=/maid/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir /maid/
WORKDIR /maid/
COPY . /maid/
RUN useradd uwsgi && chown -R uwsgi /maid

EXPOSE 8000

USER uwsgi
RUN pip install --no-cache-dir flask uwsgi

CMD [ "uwsgi", "maid-py.ini" ]
