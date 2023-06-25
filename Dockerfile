FROM python:3

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY config.json /etc/calat33/config.json

COPY . .

EXPOSE 5000/tcp

CMD [ "python", "app.py" ]
