CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"master_community_id" Nullable(Int128),
		"project_id" Nullable(Int128),
		"project_name" Nullable(Varchar(116)),
		"budget_year" Int128,
		"property_group_id" Nullable(Int128),
		"property_group_name_en" Nullable(Varchar(200)),
		"property_group_name_ar" Nullable(Varchar(266)),
		"management_company_id" Nullable(Int128),
		"management_company_name_en" Nullable(Varchar(158)),
		"management_company_name_ar" Nullable(Varchar(252)),
		"usage_id" Nullable(Int128),
		"service_category_id" Nullable(Int128),
		"service_cost" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("budget_year");