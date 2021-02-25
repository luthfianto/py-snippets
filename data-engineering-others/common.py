import datetime
import json

def pg_to_mysql(mvdict, table):
    payload=mvdict["payload"]["after"]
    myDict=payload
    if myDict.get('created_at'):
        myDict['created_at'] = myDict['created_at'].replace('T', ' ').split('.')[0]
    if myDict.get('updated_at'):
        myDict['updated_at'] = myDict['updated_at'].replace('T', ' ').split('.')[0]
    if myDict.get('due_date'):
        myDict['due_date'] = (datetime.datetime(1970,1,1) + datetime.timedelta(myDict['due_date'])).strftime('%Y-%m-%d')

    placeholders = ', '.join(['%s'] * len(myDict))
    columns = ', '.join(myDict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)

    # valid in Python 3
    valus=list(myDict.values())
    return sql, valus
