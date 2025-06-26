CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "authority_id" Nullable(Int128),
        "participant_id" Int128,
        "commerce_registry_number" Nullable(String),
        "chamber_commerce_number" Nullable(Int128),
        "rent_contract_no" Nullable(String),
        "parcel_id" Nullable(Int128),
        "main_office_id" Nullable(Int128),
        "legal_type_english" Nullable(String),
        "legal_type_arabic" Nullable(String),
        "activity_type_english" Nullable(String),
        "activity_type_arabic" Nullable(String),
        "status_english" Nullable(String),
        "status_arabic" Nullable(String),
        "license_number" Nullable(String),
        "license_issue_date" Nullable(Date),
        "license_expiry_date" Nullable(Date),
        "license_cancel_date" Nullable(Date),
        "trade_name_english" Nullable(String),
        "trade_name_arabic" Nullable(String),
        "print_rmker_arabic" Nullable(String)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("participant_id");