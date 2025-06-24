CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"master_community_id" Nullable(Integer),
		"project_id" Nullable(Integer),
		"project_name" Nullable(Varchar(116)),
		"budget_year" Integer,
		"property_group_id" Nullable(Integer),
		"property_group_name_en" Nullable(Varchar(200)),
		"property_group_name_ar" Nullable(Varchar(266)),
		"management_company_id" Nullable(Integer),
		"management_company_name_en" Nullable(Varchar(158)),
		"management_company_name_ar" Nullable(Varchar(252)),
		"usage_id" Nullable(Integer),
		"service_category_id" Nullable(Integer),
		"service_cost" Nullable(Integer)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("budget_year");