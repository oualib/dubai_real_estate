CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "request_date" Nullable(Date),
        "request_id" Int128,
        "request_source_name_english" Nullable(String),
        "request_source_name_arabic" Nullable(String),
        "application_name_english" Nullable(String),
        "application_name_arabic" Nullable(String),
        "procedure_name_english" Nullable(String),
        "procedure_name_arabic" Nullable(String),
        "property_type_english" Nullable(String),
        "property_type_arabic" Nullable(String),
        "no_of_siteplans" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("request_id");