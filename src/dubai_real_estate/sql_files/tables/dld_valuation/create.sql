CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"procedure_number" Nullable(Int128),
		"procedure_year" Nullable(Int128),
		"instance_date" Nullable(Date),
		"area_id" Int128,
		"property_type_id" Nullable(Int128),
		"property_sub_type_id" Nullable(Int128),
		"row_status_code" Nullable(Varchar(20)),
		"procedure_area" Nullable(Float),
		"actual_area" Nullable(Float),
		"property_total_value" Nullable(Float),
		"actual_worth" Nullable(Float)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("area_id");