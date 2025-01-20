FROM python:3.13.1-bullseye

RUN mkdir -p /opt/service

WORKDIR /opt/service

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

COPY bin bin
COPY lib lib

ENV PYTHONPATH="/opt/service/lib:${PYTHONPATH}"

CMD ["/opt/service/bin/bsky.py"]
