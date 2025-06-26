CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "company_name_english" String,
        "company_name_arabic" Nullable(String),
        "latitude" Nullable(Float32),
        "longitude" Nullable(Float32),
        "email" Nullable(String),
        "phone" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("company_name_english");