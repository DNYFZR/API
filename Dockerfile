# Install Python image
FROM python:3.9
# Set API base dir
WORKDIR /
# Copy requirements to image dir (enables Docker caching)
COPY ./requirements.txt /requirements.txt
# Update pip and install requirements
RUN python -m pip install --no-cache-dir --upgrade pip -r /requirements.txt
# Copy API repo to image
COPY ./api /api
# Run API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]