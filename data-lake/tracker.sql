CREATE EXTERNAL TABLE `trackerv2`.`events1` (
	`id` int COMMENT '',
	`properties` string COMMENT '',
	`timestamp` timestamp,
	`user_id` int COMMENT '',
	`created_at` timestamp COMMENT '',
	`distinct_id` string COMMENT '',
	`elements` string COMMENT '',
	`team_id` int COMMENT '',
	`elements_hash` string COMMENT ''
)
PARTITIONED BY (
	`_partitiondate` date,
	`event` string
)
STORED AS `PARQUET`
LOCATION 'oss://data-lake/trackerv2/events1/'
TBLPROPERTIES (
	'auto.create.location' = 'true'
)
