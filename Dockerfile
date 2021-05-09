FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN /usr/local/bin/python -m pip install --upgrade pip 
COPY . /code/
RUN pip install -r requirements.txt
