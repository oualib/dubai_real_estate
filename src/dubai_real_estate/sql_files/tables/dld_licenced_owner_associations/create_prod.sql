CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "company_name_english" String COMMENT '[PK] Owner association company name',
        "company_name_arabic" Nullable(String) COMMENT '[NAME] Owner association company name in Arabic',
        "latitude" Nullable(Float32) COMMENT '[GEO] Geographic latitude coordinate (WGS84) - for mapping applications',
        "longitude" Nullable(Float32) COMMENT '[GEO] Geographic longitude coordinate (WGS84) - for mapping applications',
        "email" Nullable(String) COMMENT '[CONTACT] Company email address',
        "phone" Nullable(Int128) COMMENT '[CONTACT] Company phone number'
) 
ENGINE = MergeTree()
PRIMARY KEY("company_name_english")
COMMENT 'Licensed owner associations for property and community management';