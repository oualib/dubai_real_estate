CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "parent_permit_id" Nullable(Int128) COMMENT '[FK] Parent permit identifier for hierarchical permits',
        "parent_service_name_english" Nullable(String) COMMENT '[REF] Parent service name for grouped permits',
        "parent_service_name_arabic" Nullable(String) COMMENT '[REF] Parent service name in Arabic',
        "permit_id" Int128 COMMENT '[PK] Unique permit identifier',
        "service_name_english" Nullable(String) COMMENT '[ENUM] Permit type: Inside Dubai (~85%), Company Service (~10%), Other Emirates (~3%), Outside UAE (~1%), Exhibitions (~1%)',
        "service_name_arabic" Nullable(String) COMMENT '[ENUM] Type of permit/service in Arabic',
        "permit_status_english" Nullable(String) COMMENT '[ENUM] Permit status: Auto Approval (~50%), Cancelled (~35%), Completed (~10%), Pending (~4%), Rejected (~1%)',
        "permit_status_arabic" Nullable(String) COMMENT '[ENUM] Current permit status in Arabic',
        "license_number" Nullable(String) COMMENT '[REF] Associated license number for permit holder',
        "start_date" Nullable(Date) COMMENT '[DATE] Permit validity start date',
        "end_date" Nullable(Date) COMMENT '[DATE] Permit validity end date',
        "exhibition_name_english" Nullable(String) COMMENT '[REF] Exhibition/event name (if applicable to Real Estate Exhibition permits)',
        "exhibition_name_arabic" Nullable(String) COMMENT '[REF] Exhibition/event name in Arabic',
        "participant_name_english" Nullable(String) COMMENT '[NAME] Permit holder/participant name',
        "participant_name_arabic" Nullable(String) COMMENT '[NAME] Permit holder/participant name in Arabic',
        "location" Nullable(String) COMMENT '[GEO] Location where permit is valid'
) 
ENGINE = MergeTree()
PRIMARY KEY("permit_id")
COMMENT 'Real estate permits, approvals, and regulatory authorizations';