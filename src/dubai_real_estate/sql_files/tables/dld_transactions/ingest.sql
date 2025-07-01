INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_VARCHAR("transaction_id") AS "transaction_id",
	FORMAT_INT("trans_group_id") AS "trans_group_id",
	FORMAT_INT("procedure_id") AS "procedure_id",
	"instance_date" AS "instance_date",
	FORMAT_INT("area_id") AS "area_id",
	FORMAT_VARCHAR("nearest_landmark_en") AS "nearest_landmark_en",
	FORMAT_VARCHAR("nearest_metro_en") AS "nearest_metro_en",
	FORMAT_VARCHAR("nearest_mall_en") AS "nearest_mall_en",
	FORMAT_INT("property_type_id") AS "property_type_id",
	FORMAT_INT("property_sub_type_id") AS "property_sub_type_id",
	FORMAT_VARCHAR("property_usage_en") AS "property_usage_en",
	FORMAT_INT("reg_type_id") AS "reg_type_id",
	FORMAT_VARCHAR("master_project_en") AS "master_project_en", 
	FORMAT_VARCHAR("master_project_ar") AS "master_project_ar",
	FORMAT_INT("project_number") AS "project_number",
	FORMAT_VARCHAR("project_name_en") AS "project_name_en",
	FORMAT_VARCHAR("project_name_ar") AS "project_name_ar",
	FORMAT_VARCHAR("building_name_en") AS "building_name_en",
	FORMAT_VARCHAR("building_name_ar") AS "building_name_ar",
	FORMAT_VARCHAR("rooms_en") AS "rooms_en",
	FORMAT_BOOL("has_parking") AS "has_parking",
	FORMAT_FLOAT("procedure_area") AS "procedure_area", 
	FORMAT_FLOAT("actual_worth") AS "actual_worth",
	FORMAT_INT("no_of_parties_role_1") AS "no_of_parties_role_1",
	FORMAT_INT("no_of_parties_role_2") AS "no_of_parties_role_2",
	FORMAT_INT("no_of_parties_role_3") AS "no_of_parties_role_3"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/3b25a6f5-9077-49d7-8a1e-bc6d5dea88fd/resource/a37511b0-ea36-485d-bccd-2d6cb24507e7/download/transactions.csv',
    'CSVWithNames'
)
SETTINGS 
    input_format_allow_errors_num = 10000,
    input_format_allow_errors_ratio = 0.01,
    input_format_skip_unknown_fields = 1,
    input_format_null_as_default = 1,
    format_csv_allow_single_quotes = 1,
    format_csv_allow_double_quotes = 1;