CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "developer_participant_id" Int128,
        "developer_number" Nullable(Int128),
        "developer_name_english" Nullable(String),
        "developer_name_arabic" Nullable(String),
        "registration_date" Nullable(Date),
        "chamber_commerce_number" Nullable(Int128),
        "legal_status_type_english" Nullable(String),
        "legal_status_type_arabic" Nullable(String),
        "license_source_name_english" Nullable(String),
        "license_source_name_arabic" Nullable(String),
        "license_type_english" Nullable(String),
        "license_type_arabic" Nullable(String),
        "license_number" Nullable(String),
        "license_issue_date" Nullable(Date),
        "license_expiry_date" Nullable(Date),
        "contact" Nullable(String),
        "phone" Nullable(Int128),
        "fax" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("developer_participant_id");