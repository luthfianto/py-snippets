from kafka import KafkaConsumer
import mysql.connector
import secret
import os


def get_connection():
    return mysql.connector.connect(
        host=secret.DB_URL,
        user=secret.DB_USERNAME,
        passwd=secret.DB_PASSWORD,
        database="master_db",
    )


conn = get_connection()
bootstrap_servers = ["69.69.69.69:9092"]

table = os.environ["table"]
topic_name = f"dbname.public.{table}"
group_id = os.environ.get('group_id') or "group2"

consumer = KafkaConsumer(
    topic_name, group_id=group_id, bootstrap_servers=bootstrap_servers
)

# Read and print message from consumer
import json
import common
import datetime
from time import sleep


def do_cud(payload):
    cursor = conn.cursor()

    if payload["op"] not in ["c", "u", "d"]:
        print("ERROR SKIPPING unsupported payload op: ", payload.get("op"))
        return
    if payload["op"] == "d":
        q = f"DELETE FROM {table} WHERE id={payload['before']['id']}"
        cursor.execute(q)
        print(datetime.datetime.now(), "Success Delete: ", q)
    elif payload["op"] == "c" or payload["op"] == "u":
        sql, valus = common.pg_to_mysql(mvdict, table,payload["op"])
        

        mydb = get_connection()
        cursor = mydb.cursor()
        cursor.execute(sql, valus)
        mydb.commit()
        cursor.close()
        mydb.close()

        if payload["op"] == "u": print(datetime.datetime.now(), "Success Update: ", sql,valus)
        if payload["op"] == "c": print(datetime.datetime.now(), "Success Insert: ", sql,valus)


def try_cud(payload):
    try:
        do_cud(payload)
    except mysql.connector.OperationalError as e:
        print(datetime.datetime.now(), "OperationalError", e)
        print("SLEEP")
        sleep(0.05)
        print("REINSERT "+ payload)
        try_cud(payload)
    except Exception as e:
        print(datetime.datetime.now(), "Exception", e)


for message in consumer:
    mv = message.value
#     print(mv)
    if mv is None:
        print(mv)
        continue
    mvdict = json.loads(mv)
    payload = mvdict["payload"]

    try_cud(payload)
