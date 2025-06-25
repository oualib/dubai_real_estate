CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"company_name_en" Varchar(192),
		"company_name_ar" Nullable(Varchar(332)),
		"phone" Nullable(Int128),
		"email" Nullable(Varchar(76)),
		"latitude" Nullable(Float),
		"longitude" Nullable(Float)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("company_name_en");