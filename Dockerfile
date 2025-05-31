FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

ARG GIT_TOKEN
ARG REPO_URL
ARG BRANCH=main

RUN git clone -b ${BRANCH} https://${GIT_TOKEN}@${REPO_URL} /app && \
    rm -rf /app/.git

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--timeout", "7200", "run:app"]
