from kafka import KafkaConsumer
import mysql.connector
import secret
import os

def get_connection():
    return mysql.connector.connect(
        host=secret.DB_URL,
        user=secret.DB_USERNAME,
        passwd=secret.DB_PASSWORD,
        database="",
    )

conn = get_connection()
cursor = conn.cursor()
bootstrap_servers=['69.69.69.69:9092']

table = os.environ['table']
topic_name = f"dbname.public.{table}"

consumer = KafkaConsumer(topic_name, group_id ='group1',bootstrap_servers = bootstrap_servers)


consumer = KafkaConsumer (topic_name, group_id ='group1',bootstrap_servers = bootstrap_servers)

# Read and print message from consumer
import json
import common
import datetime
for message in consumer:
    mv = message.value
    if mv is None:
        print(datetime.datetime.now(), mv)
        continue

    mvdict=json.loads(mv)
    payload=mvdict['payload']

    if payload['op']=='d':
        try:
            q=f"DELETE FROM {table} WHERE id={payload['before']['id']}"
            cursor.execute(q)
            print(datetime.datetime.now(), "success", q)
        except Exception as e:
            print(datetime.datetime.now(), "error", e)
            print(mv)
        continue

    if payload['op']=='c' or payload['op']=='u':
        try:
            sql, valus = common.pg_to_mysql(mvdict, table)
            cursor.execute(sql, valus)
            print(datetime.datetime.now(), "success", sql, valus)
        except Exception as e:
            print(datetime.datetime.now(), "error", e.decode('utf-8'))
            print(mv)
        continue

    print("ERROR SKIPPING unsupported payload op: ", payload.get('op'))
