CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "creation_date" Date,
        "parcel_number" Nullable(Int128),
        "property_number" Nullable(Int128),
        "master_project_id" Nullable(Int128),
        "project_id" Nullable(Int128),
        "building_name" Nullable(String),
        "building_number" Nullable(Int128),
        "bld_levels" Nullable(Int128),
        "floors" Nullable(Int128),
        "rooms_type_english" Nullable(String),
        "rooms_type_arabic" Nullable(String),
        "car_parks" Nullable(Int128),
        "elevators" Nullable(Int128),
        "swimming_pools" Nullable(Int128),
        "offices" Nullable(Int128),
        "shops" Nullable(Int128),
        "flats" Nullable(Int128),
        "built_up_area" Nullable(Float32),
        "actual_area" Nullable(Float32),
        "common_area" Nullable(Float32),
        "actual_common_area" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("creation_date");