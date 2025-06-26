CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "master_community_name_english" Nullable(String),
        "master_community_name_arabic" Nullable(String),
        "project_id" Nullable(Int128),
        "budget_year" Int128,
        "usage_type_english" Nullable(String),
        "usage_type_arabic" Nullable(String),
        "service_category_type_english" Nullable(String),
        "service_category_type_arabic" Nullable(String),
        "service_cost" Nullable(Int128),
        "property_group_name_english" Nullable(String),
        "property_group_name_arabic" Nullable(String),
        "management_company_name_english" Nullable(String),
        "management_company_name_arabic" Nullable(String)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("budget_year");