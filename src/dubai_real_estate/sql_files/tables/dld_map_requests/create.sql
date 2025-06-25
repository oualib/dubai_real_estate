CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"application_id" Int128,
		"procedure_id" Nullable(Int128),
		"property_type_id" Nullable(Int128),
		"request_id" Nullable(Int128),
		"request_source_id" Nullable(Int128),
		"request_date" Nullable(Date),
		"no_of_siteplans" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("application_id");