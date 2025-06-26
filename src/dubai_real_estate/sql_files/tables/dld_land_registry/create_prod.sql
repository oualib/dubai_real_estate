CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "creation_date" Date,
        "parcel_number" Nullable(Int128),
        "munc_number" Nullable(Int128),
        "munc_zip_code" Nullable(Int128),
        "area_name_english" Nullable(String),
        "area_name_arabic" Nullable(String),
        "land_property_number" Nullable(Int128),
        "land_separated_from" Nullable(Int128),
        "land_separated_reference" Nullable(Int128),
        "land_number" Nullable(Int128),
        "land_sub_number" Nullable(Int128),
        "land_type_english" Nullable(String),
        "land_type_arabic" Nullable(String),
        "master_project_id" Nullable(Int128),
        "project_id" Nullable(Int128),
        "property_sub_type_english" Nullable(String),
        "property_sub_type_arabic" Nullable(String),
        "is_free_hold" Nullable(UInt8),
        "is_registered" Nullable(UInt8),
        "pre_registration_number" Array(String),
        "actual_area" Nullable(Float64)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("creation_date");