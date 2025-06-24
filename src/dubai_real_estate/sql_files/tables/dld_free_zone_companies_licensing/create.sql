CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"fz_company_number" Integer,
		"fz_company_name_ar" Nullable(Varchar(254)),
		"fz_company_name_en" Nullable(Varchar(156)),
		"license_source_id" Nullable(Integer),
		"license_number" Nullable(Varchar(100)),
		"license_issue_date" Nullable(Date),
		"license_expiry_date" Nullable(Date),
		"email" Nullable(Varchar(74)),
		"webpage" Nullable(Varchar(60)),
		"phone" Nullable(Integer)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("fz_company_number");