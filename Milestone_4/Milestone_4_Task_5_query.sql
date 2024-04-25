WITH table_1 AS (SELECT 
	dim_store_details.store_type AS store_type,
	SUM(ROUND(CAST(orders_table.product_quantity * dim_products.product_price AS NUMERIC), 2)) AS total_sales
FROM
	orders_table
JOIN
	dim_store_details ON dim_store_details.store_code = orders_table.store_code
JOIN
	dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY
	dim_store_details.store_type)

SELECT
	store_type,
	total_sales,
	ROUND((total_sales * 100) / 7722333.64, 2) as percentage
FROM
	table_1
ORDER BY
	total_sales DESC