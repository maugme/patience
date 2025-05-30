FROM python:3.12-slim
RUN apt update && apt install -y ssh git ansible

WORKDIR /workspace