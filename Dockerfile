ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-slim
WORKDIR /opt/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
