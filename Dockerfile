# Install Python image
FROM python:3.9
# Set API base dir
WORKDIR /
# Copy requirements to image dir (enables Docker caching)
COPY ./packages/requirements.txt /packages/requirements.txt
# Update pip and install requirements
RUN python -m pip install --no-cache-dir --upgrade pip -r /packages/requirements.txt
# Copy API repo to image
COPY ./api /api
# Copy config to image
COPY ./config /config
# Run API - api.main is the fastAPI insance in the main.py script
CMD ["uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "80"]