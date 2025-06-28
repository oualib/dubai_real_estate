CREATE OR REPLACE TABLE
        "{dld_database}"."{dld_table}"(
        "fz_company_number" Int128 COMMENT '[PK] Free zone company registration number',
        "fz_company_name_english" Nullable(String) COMMENT '[NAME] Free zone company official name',
        "fz_company_name_arabic" Nullable(String) COMMENT '[NAME] Free zone company name in Arabic',
        "license_source_name_english" Nullable(String) COMMENT '[REF] Free zone authority issuing license (DIFC, DMCC, JAFZA, etc.)',
        "license_source_name_arabic" Nullable(String) COMMENT '[REF] Free zone authority name in Arabic',
        "license_number" Nullable(String) COMMENT '[REF] Free zone license number',
        "license_issue_date" Nullable(Date) COMMENT '[DATE] License issuance date',
        "license_expiry_date" Nullable(Date) COMMENT '[DATE] License expiration date',
        "email" Nullable(String) COMMENT '[CONTACT] Company email address',
        "webpage" Nullable(String) COMMENT '[CONTACT] Company website URL',
        "phone" Nullable(Int128) COMMENT '[CONTACT] Company phone number'
) 
ENGINE = MergeTree()
PRIMARY KEY("fz_company_number") COMMENT 'Free zone companies licensed for real estate activities';