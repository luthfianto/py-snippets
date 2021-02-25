FROM python:3.8-slim
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*
RUN pip install annoy
RUN pip install fastapi uvicorn mysql-connector-python pymysql joblib oss2
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
COPY . ./
ENTRYPOINT ["uvicorn","--host","0.0.0.0","--port","80","serve:app"]
