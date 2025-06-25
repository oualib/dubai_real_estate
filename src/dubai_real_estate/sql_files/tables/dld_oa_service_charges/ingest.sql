INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_INT("master_community_id") AS "master_community_id",
	FORMAT_INT("project_id") AS "project_id",
	FORMAT_VARCHAR("project_name") AS "project_name",
	FORMAT_INT("budget_year") AS "budget_year",
	FORMAT_INT("property_group_id") AS "property_group_id",
	FORMAT_VARCHAR("property_group_name_en") AS "property_group_name_en",
	FORMAT_VARCHAR("property_group_name_ar") AS "property_group_name_ar",
	FORMAT_INT("management_company_id") AS "management_company_id",
	FORMAT_VARCHAR("management_company_name_en") AS "management_company_name_en",
	FORMAT_VARCHAR("management_company_name_ar") AS "management_company_name_ar",
	FORMAT_INT("usage_id") AS "usage_id",
	FORMAT_INT("service_category_id") AS "service_category_id",
	FORMAT_INT("service_cost") AS "service_cost"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/7eadb901-4b01-4910-bc1b-a5e330da9f7c/resource/23eeac6a-f498-491a-a93b-6b16badf708b/download/oa_service_charges.csv',
    'CSVWithNames'
);