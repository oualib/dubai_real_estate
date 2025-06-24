CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"real_estate_number" UInt64,
		"participant_id" UInt64,
		"broker_number" UInt32,
		"broker_name_ar" Nullable(String),
		"broker_name_en" Nullable(String),
		"license_start_date" Date,
		"license_end_date" Date,
		"is_female" Nullable(Bool),
		"contact" Nullable(String),
		"phone" Nullable(UInt64)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("license_start_date", "license_end_date", "participant_id");