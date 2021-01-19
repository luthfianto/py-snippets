curl -i -X GET -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/some-pg-connector

curl -i -X DELETE -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/some-pg-connector

curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{ "name": "some-pg-connector", "config": { "connector.class": "io.debezium.connector.postgresql.PostgresConnector", "plugin.name": "pgoutput", "database.hostname": "", "database.port": 5432, "database.user": "", "database.password": "", "database.dbname": "my_database_name", "database.server.name": "my_database_name", "database.whitelist": "my_database_name", "database.history.kafka.bootstrap.servers": "69.69.69.69:9092", "database.history.kafka.topic": "dbhistory.my_database_name", "tasks.max": "100", "max.batch.size": 32768, "max.queue.size": 131072, "offset.flush.timeout.ms": 60000, "offset.flush.interval.ms ": 15000 } }'

curl -i -X GET -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/some-pg-connector/status
