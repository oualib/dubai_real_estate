CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "parent_permit_id" Nullable(Int128),
        "parent_service_name_english" Nullable(String),
        "parent_service_name_arabic" Nullable(String),
        "permit_id" Int128,
        "service_name_english" Nullable(String),
        "service_name_arabic" Nullable(String),
        "permit_status_english" Nullable(String),
        "permit_status_arabic" Nullable(String),
        "license_number" Nullable(String),
        "start_date" Nullable(Date),
        "end_date" Nullable(Date),
        "exhibition_name_english" Nullable(String),
        "exhibition_name_arabic" Nullable(String),
        "participant_name_english" Nullable(String),
        "participant_name_arabic" Nullable(String),
        "location" Nullable(String)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("permit_id");