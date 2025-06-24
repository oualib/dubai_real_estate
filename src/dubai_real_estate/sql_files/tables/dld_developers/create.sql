CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"participant_id" Integer,
		"developer_number" Nullable(Integer),
		"developer_name_ar" Nullable(Varchar(392)),
		"developer_name_en" Nullable(Varchar(250)),
		"chamber_commerce_number" Nullable(Integer),
		"registration_date" Nullable(Date),
		"legal_status" Nullable(Integer),
		"license_source_id" Nullable(Integer),
		"license_type_id" Nullable(Integer),
		"license_number" Nullable(Varchar(100)),
		"license_issue_date" Nullable(Date),
		"license_expiry_date" Nullable(Date),
		"contact" Nullable(Varchar(110)),
		"phone" Nullable(Integer),
		"fax" Nullable(Integer)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("participant_id");