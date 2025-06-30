CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "real_estate_number" Int128 COMMENT '[FK→dld_offices.real_estate_number] Real estate company registration number',
        "broker_name_english" Nullable(String) COMMENT '[NAME] Full name of licensed broker',
        "broker_name_arabic" Nullable(String) COMMENT '[NAME] Full name of broker in Arabic',
        "license_start_date" Nullable(Date) COMMENT '[DATE] Broker license start date',
        "license_end_date" Nullable(Date) COMMENT '[DATE] Broker license expiration date',
        "is_female" Nullable(Bool) COMMENT '[BOOL] Gender indicator (1=female, 0=male) - industry demographics tracking',
        "contact" Nullable(String) COMMENT '[CONTACT] Broker contact information',
        "phone" Nullable(Int128) COMMENT '[CONTACT] Broker phone number'
) 
ENGINE = MergeTree()
PRIMARY KEY("real_estate_number")
COMMENT 'Licensed real estate brokers and agents registry';