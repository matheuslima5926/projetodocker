FROM python:2.7
EXPOSE 5000
ADD . /code
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY university.py /code
CMD python university.py