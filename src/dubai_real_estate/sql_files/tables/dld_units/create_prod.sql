CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "creation_date" Date COMMENT '[DATE] Date when unit record was created in DLD system',
        "parcel_number" Nullable(Int128) COMMENT '[FK→dld_land_registry.parcel_number] Land parcel identifier',
        "property_number" Nullable(Int128) COMMENT '[REF] Property number assigned by DLD',
        "master_project_id" Nullable(Int128) COMMENT '[FK→dld_projects.master_project_id] Master development project identifier',
        "project_id" Nullable(Int128) COMMENT '[FK→dld_projects.project_id] Specific project identifier',
        "building_number" Nullable(String) COMMENT '[REF→dld_buildings.building_number] Building identifier where unit is located',
        "unit_number" Nullable(String) COMMENT '[REF] Specific unit number/identifier (apartment numbers, office suites)',
        "floor" Nullable(String) COMMENT '[REF] Floor level where unit is located (G, M, 1, 2, etc.)',
        "rooms_type_english" Nullable(String) COMMENT '[ENUM] Room configuration (Studio|1-10 B/R|Office|Shop|etc.) - matches market categories',
        "rooms_type_arabic" Nullable(String) COMMENT '[ENUM] Room configuration in Arabic',
        "unit_parking_number" Nullable(String) COMMENT '[REF] Assigned parking space number for unit (specific bay allocation)',
        "parking_allocation_type_english" Nullable(String) COMMENT '[ENUM] Type of parking allocation: EU (Exclusive Use), Title (Owned) - affects unit value',
        "parking_allocation_type_arabic" Nullable(String) COMMENT '[ENUM] Type of parking allocation in Arabic',
        "actual_area" Nullable(Float32) COMMENT '[UNIT:sqft] Unit interior area in square feet (carpet area)',
        "common_area" Nullable(Float32) COMMENT '[UNIT:sqft] Allocated share of common area in square feet',
        "actual_common_area" Nullable(Float32) COMMENT '[UNIT:sqft] Measured share of common area in square feet',
        "unit_balcony_area" Nullable(Float32) COMMENT '[UNIT:sqft] Balcony/terrace area in square feet - outdoor space premium'
) 
ENGINE = MergeTree()
PRIMARY KEY("creation_date")
COMMENT 'Individual property units with detailed specifications - largest property inventory';