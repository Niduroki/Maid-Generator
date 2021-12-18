FROM python:3-alpine

RUN mkdir /app/
WORKDIR /app/

ENV VIRTUAL_ENV=/app/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN adduser -S app && chown -R app /app
USER app

RUN pip install --no-cache-dir flask gunicorn

EXPOSE 8000

COPY . /app/

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "maid:app" ]
