CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "request_date" Nullable(Date) COMMENT '[DATE] Date when mapping request was submitted',
        "request_id" Int128 COMMENT '[PK] Unique mapping request identifier',
        "request_source_name_english" Nullable(String) COMMENT '[REF] Department/entity requesting the mapping service',
        "request_source_name_arabic" Nullable(String) COMMENT '[REF] Requesting department/entity in Arabic',
        "application_name_english" Nullable(String) COMMENT '[REF] Application/system name for the request',
        "application_name_arabic" Nullable(String) COMMENT '[REF] Application/system name in Arabic',
        "procedure_name_english" Nullable(String) COMMENT '[ENUM] Mapping procedure: Sell|Complete Delayed Sell|Map Issuing|Grant|Lease to Own|Ownership Transfer|etc.',
        "procedure_name_arabic" Nullable(String) COMMENT '[ENUM] Type of mapping procedure in Arabic',
        "property_type_english" Nullable(String) COMMENT '[ENUM] Property type for mapping: Unit (~50%), Land (~25%), Building (~25%)',
        "property_type_arabic" Nullable(String) COMMENT '[ENUM] Property type for mapping in Arabic',
        "no_of_siteplans" Nullable(Int128) COMMENT '[COUNT] Number of site plans requested in this mapping request'
) 
ENGINE = MergeTree()
PRIMARY KEY("request_id")
COMMENT 'Site plan and mapping documentation requests - tracks spatial documentation needs';