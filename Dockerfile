# 1. Official lightweight Python image
FROM python:3.11-slim

# 2. Set runtime working space
WORKDIR /app

# 3. Cache dependencies stage
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the raw application code files
COPY . .

# 5. Expose the port (We will map this to 8002 to avoid conflicting with str-api!)
EXPOSE 8002

# 6. Boot the ASGI server targeting main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]