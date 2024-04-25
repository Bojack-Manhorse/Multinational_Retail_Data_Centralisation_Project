SELECT 
	SUM(ROUND(CAST(orders_table.product_quantity * dim_products.product_price AS NUMERIC), 2)) AS total_sales,
	dim_store_details.store_type AS store_type,
	dim_store_details.country_code
FROM
	orders_table
JOIN
	dim_store_details ON dim_store_details.store_code = orders_table.store_code
JOIN
	dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY
	dim_store_details.store_type, dim_store_details.country_code
HAVING
	dim_store_details.country_code = 'DE'
ORDER BY
	total_sales ASC