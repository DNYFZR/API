# Fast API in a Container

Developing with FastAPI and Docker :

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
docker build -t api_image .
````

Build & run the container (adding access to localhost) :

````ps1
docker run -d --name api_container --add-host host.docker.internal:host-gateway -p 80:80 api_image:latest
````

---

## Check Web UI API Documentation

| **Docs** | **Link**
|--|--
| Main | http://localhost/docs
| Alternative | http://localhost/redoc

---

## Scripts

|**Script**|**Notes**
|--|--
|main.py| The code for the API development
|postgres.py| The code for connecting and executing queries on the PG DB
|Dockerfile| For building the docker image of the API
