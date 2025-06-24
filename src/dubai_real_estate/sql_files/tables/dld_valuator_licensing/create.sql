CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"valuation_company_number" UInt32,
		"valuation_company_name_ar" String,
		"valuation_company_name_en" String,
		"valuator_number" UInt32,
		"valuator_name_ar" String,
		"valuator_name_en" String,
		"license_start_date" Date,
		"license_end_date" Date,
		"valuator_nationality_id" UInt16,
		"is_female" Bool
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("license_start_date", "license_end_date");