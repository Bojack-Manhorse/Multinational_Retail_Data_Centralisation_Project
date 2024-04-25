SELECT 
	COUNT(locality) AS total_no_stores,
	locality
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC