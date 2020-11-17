# get arg of port
ARG APP_PORT

# default image
FROM python:3.7

# exposing port
EXPOSE ${APP_PORT}

# setting working dir
WORKDIR /current

# make dir for app
RUN mkdir -p /current/app

# packages file
COPY requirements.txt .

# updating pip
RUN pip install --upgrade pip

# install mysql python connector
RUN pip install mysqlclient

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install -r requirements.txt

# copy only the dependencies installation from the 1st stage image
COPY ./app ./app
COPY .env .
COPY run.py .

# runner application
CMD [ "python", "./run.py", "run" ]