CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "authority_id" Nullable(Int128) COMMENT '[REF] Licensing authority identifier',
        "participant_id" Int128 COMMENT '[PK] Business participant identifier',
        "commerce_registry_number" Nullable(String) COMMENT '[REF] Commerce registry registration number',
        "chamber_commerce_number" Nullable(Int128) COMMENT '[REF] Chamber of Commerce membership number',
        "rent_contract_no" Nullable(String) COMMENT '[REF] Office premises rental contract number',
        "parcel_id" Nullable(Int128) COMMENT '[FK] Land parcel where office is located',
        "main_office_id" Nullable(Int128) COMMENT '[FK→dld_offices.main_office_id] Main office identifier',
        "legal_type_english" Nullable(String) COMMENT '[ENUM] Legal entity structure type',
        "legal_type_arabic" Nullable(String) COMMENT '[ENUM] Legal entity structure type in Arabic',
        "activity_type_english" Nullable(String) COMMENT '[ENUM] Licensed business activity type',
        "activity_type_arabic" Nullable(String) COMMENT '[ENUM] Licensed business activity type in Arabic',
        "status_english" Nullable(String) COMMENT '[ENUM] Current license status (Active|Suspended|Cancelled|etc.)',
        "status_arabic" Nullable(String) COMMENT '[ENUM] Current license status in Arabic',
        "license_number" Nullable(String) COMMENT '[REF] Official business license number',
        "license_issue_date" Nullable(Date) COMMENT '[DATE] License issuance date',
        "license_expiry_date" Nullable(Date) COMMENT '[DATE] License expiration date',
        "license_cancel_date" Nullable(Date) COMMENT '[DATE] License cancellation date (if applicable)',
        "trade_name_english" Nullable(String) COMMENT '[NAME] Registered business trade name',
        "trade_name_arabic" Nullable(String) COMMENT '[NAME] Registered business trade name in Arabic',
        "print_rmker_arabic" Nullable(String) COMMENT '[REF] Print/registration marker in Arabic'
) 
ENGINE = MergeTree()
PRIMARY KEY("participant_id")
COMMENT 'Real estate business licenses and registrations';