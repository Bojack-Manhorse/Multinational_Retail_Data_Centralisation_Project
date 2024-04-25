WITH table_1 AS (
	SELECT
		year,
		CAST((timestamp - LEAD(timestamp) OVER (ORDER BY year, month, day, timestamp)) AS INTERVAL) AS time_delta
	FROM
		dim_date_times
), table_2 AS (
	SELECT
		table_1.year,
		greatest(- table_1.time_delta::interval, table_1.time_delta::interval) as time_delta
	FROM
		table_1
)

SELECT 
	table_2.year,
	AVG(table_2.time_delta) as actual_time_taken
FROM 
	table_2
GROUP BY
	table_2.year
ORDER BY
	actual_time_taken DESC