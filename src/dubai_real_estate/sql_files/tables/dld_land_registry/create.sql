CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"munc_number" Nullable(Int128),
		"munc_zip_code" Nullable(Int128),
		"area_id" Int128,
		"zone_id" Nullable(Int128),
		"parcel_id" Nullable(Int128),
		"land_number" Nullable(Int128),
		"land_sub_number" Nullable(Int128),
		"land_type_id" Nullable(Int128),
		"master_project_id" Nullable(Int128),
		"master_project_en" Nullable(Varchar(90)),
		"master_project_ar" Nullable(Varchar(150)),
		"project_id" Nullable(Int128),
		"project_name_ar" Nullable(Varchar(252)),
		"project_name_en" Nullable(Varchar(154)),
		"separated_from" Nullable(Int128),
		"separated_reference" Nullable(Int128),
		"property_id" Nullable(Int128),
		"property_sub_type_id" Nullable(Int128),
		"is_free_hold" Nullable(Bool),
		"is_registered" Nullable(Bool),
		"pre_registration_number" Nullable(Varchar(80)),
		"actual_area" Nullable(Float)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("area_id");