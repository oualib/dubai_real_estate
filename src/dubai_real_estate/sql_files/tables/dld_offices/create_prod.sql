CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "real_estate_number" Nullable(Int128) COMMENT '[FK] Real estate company registration number - links to brokers',
        "developer_participant_id" Nullable(Int128) COMMENT '[FK] Associated developer participant ID (if office is developer-affiliated)',
        "main_office_id" Int128 COMMENT '[PK] Unique office identifier',
        "license_source_name_english" Nullable(String) COMMENT '[REF] Licensing authority for the office',
        "license_source_name_arabic" Nullable(String) COMMENT '[REF] Licensing authority in Arabic',
        "license_number" Nullable(String) COMMENT '[REF] Office operation license number',
        "license_issue_date" Nullable(Date) COMMENT '[DATE] Office license issuance date',
        "license_expiry_date" Nullable(Date) COMMENT '[DATE] Office license expiration date',
        "is_branch" Nullable(Bool) COMMENT '[BOOL] Office type (1=branch office, 0=main office)',
        "activity_type_english" Nullable(String) COMMENT '[ENUM] Type of real estate activity conducted',
        "activity_type_arabic" Nullable(String) COMMENT '[ENUM] Type of real estate activity in Arabic',
        "contact_name_english" Nullable(String) COMMENT '[NAME] Office contact person name',
        "contact_name_arabic" Nullable(String) COMMENT '[NAME] Office contact person name in Arabic',
        "contact" Nullable(String) COMMENT '[CONTACT] Office contact information',
        "phone" Nullable(Int128) COMMENT '[CONTACT] Office phone number',
        "fax" Nullable(Int128) COMMENT '[CONTACT] Office fax number'
) 
ENGINE = MergeTree()
PRIMARY KEY("main_office_id")
COMMENT 'Real estate company offices and branch locations';