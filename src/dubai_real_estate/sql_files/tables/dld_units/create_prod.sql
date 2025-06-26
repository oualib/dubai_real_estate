CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "creation_date" Date,
        "parcel_number" Nullable(Int128),
        "property_number" Nullable(Int128),
        "master_project_id" Nullable(Int128),
        "project_id" Nullable(Int128),
        "building_number" Nullable(String),
        "unit_number" Nullable(String),
        "floor" Nullable(String),
        "rooms_type_english" Nullable(String),
        "rooms_type_arabic" Nullable(String),
        "unit_parking_number" Nullable(String),
        "parking_allocation_type_english" Nullable(String),
        "parking_allocation_type_arabic" Nullable(String),
        "actual_area" Nullable(Float32),
        "common_area" Nullable(Float32),
        "actual_common_area" Nullable(Float32),
        "unit_balcony_area" Nullable(Float32)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("creation_date");