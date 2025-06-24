CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"procedure_number" Nullable(Integer),
		"procedure_year" Nullable(Integer),
		"instance_date" Nullable(Date),
		"area_id" Integer,
		"property_type_id" Nullable(Integer),
		"property_sub_type_id" Nullable(Integer),
		"row_status_code" Nullable(Varchar(20)),
		"procedure_area" Nullable(Float),
		"actual_area" Nullable(Float),
		"property_total_value" Nullable(Float),
		"actual_worth" Nullable(Float)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("area_id");