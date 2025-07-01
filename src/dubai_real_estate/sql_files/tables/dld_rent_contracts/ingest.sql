INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_VARCHAR("contract_id") AS "contract_id",
	FORMAT_INT("area_id") AS "area_id",
	FORMAT_VARCHAR("nearest_landmark_en") AS "nearest_landmark_en",
	FORMAT_VARCHAR("nearest_metro_en") AS "nearest_metro_en",
	FORMAT_VARCHAR("nearest_mall_en") AS "nearest_mall_en",
	FORMAT_BOOL("is_free_hold") AS "is_free_hold",
	MAP_EJARI_BUS_PROPERTY_TYPE(FORMAT_INT("ejari_bus_property_type_id")) AS "property_type_id",
	FORMAT_VARCHAR("master_project_en") AS "master_project_en",
	FORMAT_VARCHAR("master_project_ar") AS "master_project_ar",
	FORMAT_INT("project_number") AS "project_number",
	FORMAT_VARCHAR("project_name_ar") AS "project_name_ar",
	FORMAT_VARCHAR("project_name_en") AS "project_name_en",
	FORMAT_INT("tenant_type_id") AS "tenant_type_id",
	FORMAT_INT("contract_reg_type_id") AS "contract_reg_type_id",
	FORMAT_DATE_1("contract_start_date") AS "contract_start_date",
	FORMAT_DATE_1("contract_end_date") AS "contract_end_date",
	FORMAT_INT("ejari_property_type_id") AS "ejari_property_type_id",
	FORMAT_INT("no_of_prop") AS "no_of_prop",
	FORMAT_VARCHAR("property_usage_en") AS "property_usage_en",
	FORMAT_VARCHAR("ejari_property_sub_type_en") AS "rooms_en",
	FORMAT_INT("actual_area") AS "actual_area",
	FORMAT_INT("contract_amount") AS "contract_amount",
	FORMAT_INT("annual_amount") AS "annual_amount",
	FORMAT_INT("line_number") AS "line_number"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/00768c45-f014-4cc6-937d-2b17dcab53fb/resource/765b5a69-ca16-4bfd-9852-74612f3c4ea6/download/rent_contracts.csv',
    'CSVWithNames'
)
SETTINGS 
    input_format_allow_errors_num = 10000,
    input_format_allow_errors_ratio = 0.01,
    input_format_skip_unknown_fields = 1,
    input_format_null_as_default = 1,
    format_csv_allow_single_quotes = 1,
    format_csv_allow_double_quotes = 1;