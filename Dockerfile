# pull official base image
FROM python

# copy project
COPY . .

# set work directory
WORKDIR /fabio-tests

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


