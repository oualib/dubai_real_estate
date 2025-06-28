CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "master_community_name_english" Nullable(String) COMMENT '[REF] Master community name where charges apply',
        "master_community_name_arabic" Nullable(String) COMMENT '[REF] Master community name in Arabic',
        "project_id" Nullable(Int128) COMMENT '[FK→dld_projects.project_id] Project identifier within community',
        "budget_year" Int128 COMMENT '[YEAR] Budget year for service charges',
        "usage_type_english" Nullable(String) COMMENT '[ENUM] Property usage type: Residential (~70%), Retail (~30%) - affects service charge rates',
        "usage_type_arabic" Nullable(String) COMMENT '[ENUM] Property usage type in Arabic',
        "service_category_type_english" Nullable(String) COMMENT '[ENUM] Service category: Services|Maintenance|Management|Utilities|Reserved Fund|Insurance|Master Community|Improvement',
        "service_category_type_arabic" Nullable(String) COMMENT '[ENUM] Service category in Arabic',
        "service_cost" Nullable(Int128) COMMENT '[CURRENCY:AED] Annual service charge amount in AED per sqft - varies by category and usage type',
        "property_group_name_english" Nullable(String) COMMENT '[REF] Property group classification within community',
        "property_group_name_arabic" Nullable(String) COMMENT '[REF] Property group classification in Arabic',
        "management_company_name_english" Nullable(String) COMMENT '[REF] Management company handling services',
        "management_company_name_arabic" Nullable(String) COMMENT '[REF] Management company name in Arabic'
) 
ENGINE = MergeTree()
PRIMARY KEY("budget_year")
COMMENT 'Owner association service charges and community fees by category and usage type';