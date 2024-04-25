ALTER TABLE dim_products
	RENAME removed TO still_available;

ALTER TABLE dim_products
	ALTER COLUMN product_price TYPE FLOAT,
	ALTER COLUMN weight TYPE FLOAT,
	ALTER COLUMN "EAN" TYPE VARCHAR(100),
	ALTER COLUMN product_code TYPE VARCHAR(100),
	ALTER COLUMN date_added TYPE DATE,
	ALTER COLUMN uuid TYPE uuid USING uuid::uuid,
	ALTER COLUMN still_available TYPE BOOL USING still_available::boolean,
	ALTER COLUMN weight_class TYPE VARCHAR(14)