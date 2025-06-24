CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"procedure_number" UInt16,
		"procedure_year" UInt16,
		"instance_date" Nullable(Date),
		"area_id" UInt16,
		"property_type_id" UInt8,
		"property_sub_type_id" UInt16,
		"row_status_code" LowCardinality(String),
		"procedure_area" Decimal(13,3),
		"actual_area" Decimal(13,3),
		"property_total_value" Decimal(16,3),
		"actual_worth" Decimal(16,3)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("area_id", "property_type_id", "property_sub_type_id", "row_status_code");