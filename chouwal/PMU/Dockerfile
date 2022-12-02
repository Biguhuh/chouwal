FROM --platform=linux/amd64 tensorflow/tensorflow:2.10.0
FROM python3.10.8-buster

#FROM: select a base image for our image (the environment in which we will run our code), this is usually the first instruction
#COPY: copy files and directories into our image (our package and the associated files, for example)
#RUN: execute a command inside of the image being built (for example, pip install -r requirements.txt to install package dependencies)
#CMD: the main command that will be executed when we run our Docker image. There can only be one CMD instruction in a Dockerfile. It is usually the last instruction!

COPY requirements /requirements_prod.txt
COPY pmu_breaking /pmu_breaking
RUN pip install -r requirements_prod.txt
CMD uvicorn taxifare.api.fast:app --host 0.0.0.0
