CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "creation_date" Date COMMENT '[DATE] Date when land record was created in DLD system',
        "parcel_number" Nullable(Int128) COMMENT '[PK→buildings.parcel_number|PK→units.parcel_number] Unique land parcel identifier - joins to buildings and units',
        "munc_number" Nullable(Int128) COMMENT '[REF] Municipality area number for administrative jurisdiction',
        "munc_zip_code" Nullable(Int128) COMMENT '[REF] Municipality postal/zip code',
        "area_name_english" Nullable(String) COMMENT '[GEO] Geographic area/district name - consistent with transactions/rentals',
        "area_name_arabic" Nullable(String) COMMENT '[GEO] Geographic area/district name in Arabic',
        "land_property_number" Nullable(Int128) COMMENT '[REF→dld_projects.land_property_number] Land property registration number',
        "land_separated_from" Nullable(Int128) COMMENT '[REF→dld_land_registry.parcel_number] Original parcel number if land was subdivided from larger plot',
        "land_separated_reference" Nullable(Int128) COMMENT '[REF→dld_land_registry.land_property_number] Reference number for land subdivision process',
        "land_number" Nullable(Int128) COMMENT '[REF] Primary land plot number',
        "land_sub_number" Nullable(Int128) COMMENT '[REF] Sub-plot number for subdivided land',
        "land_type_english" Nullable(String) COMMENT '[ENUM] Land classification type (Residential|Commercial|Mixed|Industrial|etc.)',
        "land_type_arabic" Nullable(String) COMMENT '[ENUM] Land classification type in Arabic',
        "master_project_id" Nullable(Int128) COMMENT '[FK] Master development project if applicable',
        "project_id" Nullable(Int128) COMMENT '[FK→dld_projects.project_id] Specific project if land is part of development',
        "property_sub_type_english" Nullable(String) COMMENT '[ENUM] Detailed property subcategory',
        "property_sub_type_arabic" Nullable(String) COMMENT '[ENUM] Detailed property subcategory in Arabic',
        "is_free_hold" Nullable(UInt8) COMMENT '[BOOL] Ownership type (1=freehold, 0=leasehold) - affects foreign ownership eligibility',
        "is_registered" Nullable(UInt8) COMMENT '[BOOL] Registration status (1=registered, 0=pending)',
        "pre_registration_number" Array(String) COMMENT '[ARRAY] List of pre-registration reference numbers (ClickHouse Array type)',
        "actual_area_sqm" Nullable(Float64) COMMENT '[UNIT:sqm] Measured land area in square meter by Dubai Municipality'
) 
ENGINE = MergeTree()
PRIMARY KEY("creation_date")
COMMENT 'Official land parcel registry with ownership and zoning details';