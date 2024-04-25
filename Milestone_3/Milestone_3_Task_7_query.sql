ALTER TABLE dim_card_details
	ALTER COLUMN card_number TYPE VARCHAR(22),
	ALTER COLUMN expiry_date TYPE DATE,
	ALTER COLUMN date_payment_confirmed TYPE DATE