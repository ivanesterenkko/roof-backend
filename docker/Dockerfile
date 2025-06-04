FROM python:3.12.0-slim-bookworm

RUN mkdir /roof_api

WORKDIR /roof_api

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN python -m pip install --no-cache-dir uv \
    && uv export --no-hashes --format requirements.txt -o requirements.txt

RUN mkdir -p wheels \
    && pip wheel --no-cache-dir --no-deps -r requirements.txt -w wheels \
    && ls -l wheels \
    && test "$(ls -A wheels)" || (echo "No wheels built!" && exit 1)


RUN pip install --no-cache-dir wheels/*.whl

COPY . .

ENV PYTHONPATH=/roof_api
