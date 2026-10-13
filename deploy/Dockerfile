FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir .

ENV MUSEFORGE_HOST=0.0.0.0
ENV MUSEFORGE_PORT=8000

EXPOSE 8000

CMD ["python", "-m", "museforge.cli", "serve"]
