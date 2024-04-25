SELECT 
	dim_date_times.month AS month,
	SUM(ROUND(CAST(orders_table.product_quantity * dim_products.product_price AS NUMERIC), 2)) AS total_sales
FROM
	dim_date_times
JOIN
	orders_table ON orders_table.date_uuid = dim_date_times.date_uuid
JOIN
	dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY 
	month
ORDER BY
	total_sales DESC