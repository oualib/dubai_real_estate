CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"participant_id" UInt64,
		"developer_number" UInt16,
		"developer_name_ar" String,
		"developer_name_en" String,
		"chamber_commerce_number" UInt32,
		"registration_date" Date,
		"legal_status" UInt32,
		"license_source_id" UInt16,
		"license_type_id" UInt32,
		"license_type_extract" Nullable(String),
		"license_number" Nullable(UInt64),
		"license_issue_date" Date,
		"license_expiry_date" Date,
		"contact" String,
		"phone" UInt64,
		"fax" UInt64
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("developer_number", "participant_id");