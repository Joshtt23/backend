FROM python:3.10-slim-bullseye 


COPY . /sabc_bot 
WORKDIR /sabc_bot

RUN apt-get update && apt-get install -y git

RUN python3.10 -m pip install -r ./requirements.txt  

EXPOSE 8888

ENTRYPOINT ["python", "-m", "sabc_bot"]
 