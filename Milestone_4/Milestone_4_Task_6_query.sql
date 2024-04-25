SELECT 
	SUM(ROUND(CAST(orders_table.product_quantity * dim_products.product_price AS NUMERIC), 2)) AS total_sales,
	dim_date_times.year,
	dim_date_times.month
FROM
	orders_table
JOIN
	dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid
JOIN
	dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY
	dim_date_times.month, dim_date_times.year
ORDER BY
	total_sales DESC