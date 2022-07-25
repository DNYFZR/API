# API Development

This project is focused on developing REST APIs for backend development.

Dev tools :

- FastAPI
- Docker
- Postgres DB (psycopg2 Python connector)
- Azure SQL DB (pyodbc Python connector)

---

## Codebase

The durrent project was developed with FastAPI in Python.

The codebase consists of the following scripts :

|**Script**|**Notes**
|--|--
|main.py| The code for the API development
|pipelines.py| Pipeline code for accessing databases. Currently Postgres & Azure.
|Dockerfile| For building the docker image of the API

---

## Environment Set-up

In this project a virtual environment has been used, as shown below.

````ps1
# Set up project
mkdir Fast-API-Project && cd Fast-API-Project

# Setup environment
python -m venv fast_api_env
cd scripts 
activate

# Install dependencies
python -m pip install --upgrade pip
python -m pip install psycopg2
python -m pip install pyodbc
python -m pip install pandas
python -m pip install fastapi uvicorn[standard]

# Set up repo
cd ../../
mkdir Fast-API && cd Fast-API

# Generate an inital requirements file
python -m pip freeze > requirements.txt
````

At this point we have a Fast-API-Project file, which contains a fast_api_env virtual environment, and Fast-API, contianing the basic requirements file for the project.  

---

## Docker

Docker has been used in this project to package the API code into a production ready format.

When the project is ready to deploy, build the image :

````ps1
docker build -t api_image .
````

Then, build & run the container (adding access to localhost) :

````ps1
docker run -d --name api_container --add-host host.docker.internal:host-gateway -p 80:80 api_image:latest
````

---

## Web UI API Documentation

One of the main reasons to use FastAPI is the web interface, the docs being a great example.

When running an API locally :

| **Docs** | **Link**
|--|--
| Main | http://localhost/docs
| Alternative | http://localhost/redoc
