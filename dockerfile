FROM python:3.9

WORKDIR /app
COPY . ./

RUN pip install -U git+https://github.com/Pycord-Development/pycord
RUN pip install -r requirements.txt

CMD ["python", "main.py"]