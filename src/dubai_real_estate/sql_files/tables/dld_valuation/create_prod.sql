CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "procedure_number" Nullable(Int128),
        "row_status_code" Nullable(String),
        "procedure_year" Int128,
        "instance_date" Nullable(Date),
        "area_name_english" Nullable(String),
        "area_name_arabic" Nullable(String),
        "property_type_english" Nullable(String),
        "property_type_arabic" Nullable(String),
        "property_sub_type_english" Nullable(String),
        "property_sub_type_arabic" Nullable(String),
        "procedure_area" Nullable(Float32),
        "actual_area" Nullable(Float32),
        "property_total_value" Nullable(Float32),
        "actual_worth" Nullable(Float32)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("procedure_year");