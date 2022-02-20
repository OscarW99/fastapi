FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# This will copy all files (source code) in our current directoy to the workdir in our container
COPY . .

CMD ["uvicorn", "app.main:app", "--host:", "0.0.0.0", "--port", "8000"]

# https://hub.docker.com/_/python


## to run in terminal...
# docker build --help
## -t is a tag. The '.' tell docker what directory the docker file is in (current dir)
# docker build -t fastapi .
# docker image ls
## You can use docker from the CLI however you can also use docker compose which is where you write all docker commands in a file and then run the file.