FROM python:3.9-slim-bookworm
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# set work directory
WORKDIR /app

# Набор для сборки psycopg2 (gcc+libpq-dev) и диагностики
RUN export DEBIAN_FRONTEND=noninteractive \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential=12.* \
      libpq-dev=15.* \
      dnsutils=1:9.18.* \
 && rm -rf /var/lib/apt/lists/*

# 13 Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#18 Install dependencies
RUN python -m pip install --no-cache-dir pip==22.0.4

RUN useradd -m -U -s /usr/sbin/nologin app

#24 copy project
COPY --chown=app:app requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY --chown=app:app . /app/

# install pygoat
EXPOSE 8000

USER app
WORKDIR /app/pygoat/
CMD ["gunicorn","--bind","0.0.0.0:8000","--workers","6","pygoat.wsgi"]
