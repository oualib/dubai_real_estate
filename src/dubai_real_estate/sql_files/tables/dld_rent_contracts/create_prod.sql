CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "contract_id" String COMMENT '[PK] Unique rental contract identifier',
        "contract_reg_type_english" Nullable(String) COMMENT '[ENUM] Contract registration type: New (~60%), Renew (~40%) - tracks market turnover',
        "contract_reg_type_arabic" Nullable(String) COMMENT '[ENUM] Contract registration type in Arabic',
        "contract_start_date" Nullable(Date) COMMENT '[DATE] Rental contract start date - essential for lease period analysis',
        "contract_end_date" Nullable(Date) COMMENT '[DATE] Rental contract end date - used for renewal tracking',
        "area_name_english" Nullable(String) COMMENT '[GEO] Geographic area/district of rental property - matches transaction areas',
        "area_name_arabic" Nullable(String) COMMENT '[GEO] Geographic area/district in Arabic',
        "nearest_landmark_name_english" Nullable(String) COMMENT '[GEO] Closest landmark to rental property',
        "nearest_landmark_name_arabic" Nullable(String) COMMENT '[GEO] Closest landmark in Arabic',
        "nearest_metro_name_english" Nullable(String) COMMENT '[GEO] Nearest Metro station to rental property - premium for metro accessibility',
        "nearest_metro_name_arabic" Nullable(String) COMMENT '[GEO] Nearest Metro station in Arabic',
        "nearest_mall_name_english" Nullable(String) COMMENT '[GEO] Nearest shopping mall to rental property',
        "nearest_mall_name_arabic" Nullable(String) COMMENT '[GEO] Nearest shopping mall in Arabic',
        "property_type_english" Nullable(String) COMMENT '[ENUM] Type of rental property (Multiple|Villa|Apartment|etc.)',
        "property_type_arabic" Nullable(String) COMMENT '[ENUM] Type of rental property in Arabic',
        "ejari_property_type_english" Nullable(String) COMMENT '[ENUM] Official Ejari property classification for government registration',
        "ejari_property_type_arabic" Nullable(String) COMMENT '[ENUM] Official Ejari property classification in Arabic',
        "property_usage_type_english" Nullable(String) COMMENT '[ENUM] Intended usage (Residential|Commercial|Mixed|Industrial|etc.)',
        "property_usage_type_arabic" Nullable(String) COMMENT '[ENUM] Intended usage in Arabic',
        "master_project_id" Nullable(Int128) COMMENT '[FK] Link to master development project',
        "project_id" Nullable(Int128) COMMENT '[FK] Link to specific project',
        "is_free_hold" Nullable(Bool) COMMENT '[BOOL] Property ownership type (1=freehold, 0=leasehold) - affects rental dynamics',
        "tenant_type_english" Nullable(String) COMMENT '[ENUM] Type of tenant: Person (~95%), Company (~5%) - individual vs corporate rentals',
        "tenant_type_arabic" Nullable(String) COMMENT '[ENUM] Type of tenant in Arabic',
        "line_number" Nullable(Int128) COMMENT '[REF] Line item number in multi-unit contracts (bulk rental agreements)',
        "no_of_prop" Nullable(Int128) COMMENT '[COUNT] Number of properties in the contract (typically 1 for individual leases)',
        "rooms_type_english" Nullable(String) COMMENT '[ENUM] Room config: 1-2 B/R most common, Office, Studio, Labor Camp, Warehouse, Shop, Restaurant, etc.',
        "rooms_type_arabic" Nullable(String) COMMENT '[ENUM] Room configuration in Arabic',
        "actual_area_sqm" Nullable(Int128) COMMENT '[UNIT:sqm] Actual rental area in square meter',
        "contract_amount" Nullable(Int128) COMMENT '[CURRENCY:AED] Total contract value in AED (may include multi-year amounts)',
        "annual_amount" Nullable(Int128) COMMENT '[CURRENCY:AED] Annual rental amount in AED - key metric for yield analysis'
) 
ENGINE = MergeTree()
PRIMARY KEY("contract_id")
COMMENT 'Official rental contracts and Ejari registrations in Dubai - largest table in database';