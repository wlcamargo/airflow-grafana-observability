FROM python:3.12-slim

WORKDIR /app

COPY src/ /app/
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["bash"]