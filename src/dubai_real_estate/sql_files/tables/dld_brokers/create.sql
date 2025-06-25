CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"real_estate_number" Int128,
		"participant_id" Nullable(Int128),
		"broker_number" Nullable(Int128),
		"broker_name_ar" Nullable(Varchar(268)),
		"broker_name_en" Nullable(Varchar(150)),
		"license_start_date" Nullable(Date),
		"license_end_date" Nullable(Date),
		"is_female" Nullable(Bool),
		"contact" Nullable(Varchar(102)),
		"phone" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("real_estate_number");