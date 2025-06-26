CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
		"valuation_company_number" Int128,
		"valuation_company_name_english" Nullable(String),
		"valuation_company_name_arabic" Nullable(String),
		"valuator_number" Nullable(Int128),
		"valuator_name_english" Nullable(String),
		"valuator_name_arabic" Nullable(String),
		"license_start_date" Nullable(Date),
		"license_end_date" Nullable(Date),
		"valuator_nationality_english" Nullable(String),
		"valuator_nationality_arabic" Nullable(String),
		"is_female" Nullable(Bool)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("valuation_company_number");