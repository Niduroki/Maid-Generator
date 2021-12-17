FROM python:3-alpine

RUN apk add --no-cache gcc libc-dev linux-headers

RUN mkdir /maid/
WORKDIR /maid/

ENV VIRTUAL_ENV=/maid/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . /maid/
RUN adduser -S uwsgi && chown -R uwsgi /maid

EXPOSE 8000

USER uwsgi
RUN pip install --no-cache-dir flask uwsgi

CMD [ "uwsgi", "maid-py.ini" ]
