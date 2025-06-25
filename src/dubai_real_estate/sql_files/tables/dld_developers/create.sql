CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"participant_id" Int128,
		"developer_number" Nullable(Int128),
		"developer_name_ar" Nullable(Varchar(392)),
		"developer_name_en" Nullable(Varchar(250)),
		"chamber_commerce_number" Nullable(Int128),
		"registration_date" Nullable(Date),
		"legal_status" Nullable(Int128),
		"license_source_id" Nullable(Int128),
		"license_type_id" Nullable(Int128),
		"license_number" Nullable(Varchar(100)),
		"license_issue_date" Nullable(Date),
		"license_expiry_date" Nullable(Date),
		"contact" Nullable(Varchar(110)),
		"phone" Nullable(Int128),
		"fax" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("participant_id");