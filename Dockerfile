FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api .
COPY ./sheep.png .

EXPOSE 5000

CMD [ "python", "./api.py" ]