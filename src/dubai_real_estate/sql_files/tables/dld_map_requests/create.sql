CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"application_id" Integer,
		"procedure_id" Nullable(Integer),
		"property_type_id" Nullable(Integer),
		"request_id" Nullable(Integer),
		"request_source_id" Nullable(Integer),
		"request_date" Nullable(Date),
		"no_of_siteplans" Nullable(Integer)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("application_id");