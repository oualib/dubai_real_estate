CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"valuation_company_number" Int128,
		"valuation_company_name_ar" Nullable(Varchar(258)),
		"valuation_company_name_en" Nullable(Varchar(258)),
		"valuator_number" Nullable(Int128),
		"valuator_name_ar" Nullable(Varchar(148)),
		"valuator_name_en" Nullable(Varchar(96)),
		"license_start_date" Nullable(Date),
		"license_end_date" Nullable(Date),
		"valuator_nationality_id" Nullable(Int128),
		"is_female" Nullable(Bool)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("valuation_company_number");