CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "fz_company_number" Int128,
        "fz_company_name_english" Nullable(String),
        "fz_company_name_arabic" Nullable(String),
        "license_source_name_english" Nullable(String),
        "license_source_name_arabic" Nullable(String),
        "license_number" Nullable(String),
        "license_issue_date" Nullable(Date),
        "license_expiry_date" Nullable(Date),
        "email" Nullable(String),
        "webpage" Nullable(String),
        "phone" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("fz_company_number");