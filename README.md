# Fast API in a Container

Developing with FastAPI and Docker.

---

## Set-up

````ps1
# Setup environment
python -m venv fast_api_env
cd scripts 
activate

# Install dependencies
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn[standard]

# Generate a requirements file
python -m pip freeze > requirements.txt
````

Running the API for the first time

````ps1
# Test the API with UVICORN Server
uvicorn main:app --reload

````

---

## Docker

To build the image :

````ps1
docker build -t fast_api_001 .
````

Build & run the container :

````ps1
docker run -d --name api_dev -p 80:80 fast_api_001
````

---

## Check Web UI API Documentation

| **Docs** | **Link**
|--|--
| Main | http://localhost/docs
| Alternative | http://localhost/redoc

---
