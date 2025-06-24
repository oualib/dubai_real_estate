CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"munc_number" Nullable(Integer),
		"munc_zip_code" Nullable(Integer),
		"area_id" Integer,
		"zone_id" Nullable(Integer),
		"parcel_id" Nullable(Integer),
		"land_number" Nullable(Integer),
		"land_sub_number" Nullable(Integer),
		"land_type_id" Nullable(Integer),
		"master_project_id" Nullable(Integer),
		"master_project_en" Nullable(Varchar(90)),
		"master_project_ar" Nullable(Varchar(150)),
		"project_id" Nullable(Integer),
		"project_name_ar" Nullable(Varchar(252)),
		"project_name_en" Nullable(Varchar(154)),
		"separated_from" Nullable(Integer),
		"separated_reference" Nullable(Integer),
		"property_id" Nullable(Integer),
		"property_sub_type_id" Nullable(Integer),
		"is_free_hold" Nullable(Bool),
		"is_registered" Nullable(Bool),
		"pre_registration_number" Nullable(Varchar(80)),
		"actual_area" Nullable(Float)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("area_id");