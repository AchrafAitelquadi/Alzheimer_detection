# app/Dockerfile
FROM python:3.12

WORKDIR /app

# Copy the requirements.txt file from the parent folder (above the app/ folder)
COPY requirements.txt /app/requirements.txt

# Copy all files from the app folder to the /app folder in the container
COPY ./app /app

RUN pip install --upgrade pip && \
    pip install --default-timeout=100 --retries=10 -r /app/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]