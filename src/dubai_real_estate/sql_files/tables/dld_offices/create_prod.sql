CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "real_estate_number" Nullable(Int128),
        "developer_participant_id" Nullable(Int128),
        "main_office_id" Int128,
        "license_source_name_english" Nullable(String),
        "license_source_name_arabic" Nullable(String),
        "license_number" Nullable(String),
        "license_issue_date" Nullable(Date),
        "license_expiry_date" Nullable(Date),
        "is_branch" Nullable(Bool),
        "activity_type_english" Nullable(String),
        "activity_type_arabic" Nullable(String),
        "contact_name_english" Nullable(String),
        "contact_name_arabic" Nullable(String),
        "contact" Nullable(String),
        "phone" Nullable(Int128),
        "fax" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("main_office_id");