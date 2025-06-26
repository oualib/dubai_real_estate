CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "real_estate_number" Int128,
        "broker_id" Nullable(Int128),
        "license_start_date" Nullable(Date),
        "license_end_date" Nullable(Date),
        "broker_name_english" Nullable(String),
        "broker_name_arabic" Nullable(String),
        "is_female" Nullable(Bool),
        "contact" Nullable(String),
        "phone" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("real_estate_number");