CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"main_office_id" Integer,
		"is_branch" Nullable(Bool),
		"real_estate_number" Nullable(Integer),
		"participant_id" Nullable(Integer),
		"activity_type_id" Nullable(Integer),
		"license_source_id" Nullable(Integer),
		"license_number" Nullable(Varchar(100)),
		"license_issue_date" Nullable(Date),
		"license_expiry_date" Nullable(Date),
		"contact_name_en" Nullable(Varchar(102)),
		"contact_name_ar" Nullable(Varchar(102)),
		"contact" Nullable(Varchar(102)),
		"mobile" Nullable(Integer),
		"phone" Nullable(Integer),
		"fax" Nullable(Integer)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("main_office_id");