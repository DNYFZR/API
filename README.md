<h1 align="center"><b> 🎡 API Repo 🎡 </b></h1>
<br/>

<h3 align="center"><b> Containerised REST API Development</b></h3>
<br/>
 
---
<br/>

## ⚾ Codebase

The durrent project was developed with FastAPI in Python.

The codebase consists of the following scripts :

|**Script**|**Notes**
|--|--
| [main](api/main.py) | The main API deployment codebase.
| [database](api/database.py) | Pipeline code for accessing databases. <br/> (Currently Postgres & Azure / SQL Server)
| [query](/api/query.py) | Module for building query strings from API parameters.
| [Dockerfile](/Dockerfile)| For building the docker image of the API.

---
<br/>

## 🐳 Docker


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
<br/>

## 🌿 Environment Set-up

The project is primarily being developed using :

- Python 3.9
- FastAPI
- Docker
- SQLAlchemy

In this project a virtual environment has been used, as shown below.

````ps1
# Set up project
mkdir Fast-API-Project && cd Fast-API-Project
r
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
