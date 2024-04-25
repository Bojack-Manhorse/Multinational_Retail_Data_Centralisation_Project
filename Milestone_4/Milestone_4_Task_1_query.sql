SELECT 
	COUNT(country_code) AS total_no_stores,
	country_code
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC