CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "developer_participant_id" Int128 COMMENT '[PK] Unique developer participant identifier',
        "developer_number" Nullable(Int128) COMMENT '[PK|JOIN] Developer registration number - joins to dld_projects.developer_number',
        "developer_name_english" Nullable(String) COMMENT '[NAME] Official developer company name',
        "developer_name_arabic" Nullable(String) COMMENT '[NAME] Official developer company name in Arabic',
        "registration_date" Nullable(Date) COMMENT '[DATE] Developer registration date with DLD',
        "chamber_commerce_number" Nullable(Int128) COMMENT '[REF] Chamber of Commerce registration number',
        "legal_status_type_english" Nullable(String) COMMENT '[ENUM] Legal entity type: Limited Responsibility (~60%), Off Shore (~15%), Personal (~5%), etc.',
        "legal_status_type_arabic" Nullable(String) COMMENT '[ENUM] Legal entity type in Arabic',
        "license_source_name_english" Nullable(String) COMMENT '[REF] Licensing authority name',
        "license_source_name_arabic" Nullable(String) COMMENT '[REF] Licensing authority name in Arabic',
        "license_type_english" Nullable(String) COMMENT '[ENUM] License type: Commercial (~65%), Professional (~15%), Others (~20%)',
        "license_type_arabic" Nullable(String) COMMENT '[ENUM] Type of development license in Arabic',
        "license_number" Nullable(String) COMMENT '[REF] Official license number',
        "license_issue_date" Nullable(Date) COMMENT '[DATE] License issuance date',
        "license_expiry_date" Nullable(Date) COMMENT '[DATE] License expiration date - track license validity',
        "contact" Nullable(String) COMMENT '[CONTACT] Primary contact information (email/address)',
        "phone" Nullable(Int128) COMMENT '[CONTACT] Primary phone number',
        "fax" Nullable(Int128) COMMENT '[CONTACT] Fax number for official communications'
) 
ENGINE = MergeTree()
PRIMARY KEY("developer_participant_id")
COMMENT 'Licensed real estate developers registry with legal and contact details';