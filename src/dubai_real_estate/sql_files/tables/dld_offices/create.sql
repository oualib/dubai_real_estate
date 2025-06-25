CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"main_office_id" Int128,
		"is_branch" Nullable(Bool),
		"real_estate_number" Nullable(Int128),
		"participant_id" Nullable(Int128),
		"activity_type_id" Nullable(Int128),
		"license_source_id" Nullable(Int128),
		"license_number" Nullable(Varchar(100)),
		"license_issue_date" Nullable(Date),
		"license_expiry_date" Nullable(Date),
		"contact_name_en" Nullable(Varchar(102)),
		"contact_name_ar" Nullable(Varchar(102)),
		"contact" Nullable(Varchar(102)),
		"mobile" Nullable(Int128),
		"phone" Nullable(Int128),
		"fax" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("main_office_id");