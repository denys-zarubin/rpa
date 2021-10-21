FROM python:3
WORKDIR /code
COPY requirements.txt . 
RUN pip install --no-cache -r requirements.txt
COPY . /code/
CMD ["tail", "-f", "requirements.txt"]