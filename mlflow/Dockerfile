FROM python:3.9

WORKDIR /app
RUN pip install mlflow

# Copy your local mlruns directory into the container
COPY mlruns /app/mlruns

# Optionally expose the MLflow port
EXPOSE 5000

# Default command (you can override it in docker-compose if needed)
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000", "--default-artifact-root", "/mlruns", "--serve-artifacts"]
