CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "creation_date" Date COMMENT '[DATE] Date when building record was created in DLD system',
        "parcel_number" Nullable(Int128) COMMENT '[FK→dld_land_registry.parcel_number] Land parcel identifier where building is located',
        "property_number" Nullable(Int128) COMMENT '[REF|UNIQUE] Unique property number assigned by DLD',
        "master_project_id" Nullable(Int128) COMMENT '[FK→dld_projects.master_project_id] Master development project identifier',
        "project_id" Nullable(Int128) COMMENT '[FK→dld_projects.project_id] Specific project identifier within master project',
        "building_name" Nullable(String) COMMENT '[REF] Official building name or identifier (often tower/building names)',
        "building_number" Nullable(Int128) COMMENT '[REF] Numeric building identifier within project',
        "bld_levels" Nullable(Int128) COMMENT '[COUNT] Total number of building levels (including basement and podium levels)',
        "floors" Nullable(Int128) COMMENT '[COUNT] Number of floors above ground level (excludes basement/podium)',
        "rooms_type_english" Nullable(String) COMMENT '[ENUM] Primary room configuration type in building (indicates building purpose)',
        "rooms_type_arabic" Nullable(String) COMMENT '[ENUM] Primary room configuration type in Arabic',
        "car_parks" Nullable(Int128) COMMENT '[COUNT] Number of parking spaces available - critical amenity metric',
        "elevators" Nullable(Int128) COMMENT '[COUNT] Number of elevators in building - affects unit accessibility and value',
        "swimming_pools" Nullable(Int128) COMMENT '[COUNT] Number of swimming pools in building - premium amenity indicator',
        "offices" Nullable(Int128) COMMENT '[COUNT] Number of office units in building (mixed-use indicator)',
        "shops" Nullable(Int128) COMMENT '[COUNT] Number of retail/shop units in building (ground floor commercial)',
        "flats" Nullable(Int128) COMMENT '[COUNT] Number of residential apartment units',
        "built_up_area_sqm" Nullable(Float32) COMMENT '[UNIT:sqm] Total built-up area of building in square meter (gross floor area)',
        "actual_area_sqm" Nullable(Float32) COMMENT '[UNIT:sqm] Actual usable area in square meter (net floor area)',
        "common_area_sqm" Nullable(Float32) COMMENT '[UNIT:sqm] Shared/common area in square meter (lobbies, corridors, amenities)',
        "actual_common_area_sqm" Nullable(Int128) COMMENT '[UNIT:sqm] Actual measured common area in square meter'
) 
ENGINE = MergeTree()
PRIMARY KEY("creation_date")
COMMENT 'Physical building registry with specifications and amenities - architectural database';