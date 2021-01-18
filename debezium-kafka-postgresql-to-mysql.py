from kafka import KafkaConsumer
import mysql.connector
import secret

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

topic_name = 'db.public.table'
table = 'table'
# Initialize consumer variable
consumer = KafkaConsumer (topic_name, group_id ='group1',bootstrap_servers = bootstrap_servers)

# Read and print message from consumer
import json
for message in consumer:
    try:
        mv = message.value
        mvdict=json.loads(mv)
        payload=mvdict["payload"]["after"]
        myDict=payload
        myDict['created_at'] = myDict['created_at'].replace('T', ' ')[:-8]
        myDict['updated_at'] = myDict['updated_at'].replace('T', ' ')[:-8]

        placeholders = ', '.join(['%s'] * len(myDict))
        columns = ', '.join(myDict.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)

        # valid in Python 3
        valus=list(myDict.values())
        print(sql, valus)
        cursor.execute(sql, valus)
    except Error as e:
        print("error", e)
