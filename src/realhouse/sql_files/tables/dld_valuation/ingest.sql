INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT 
	FORMAT_INT("procedure_number") AS "procedure_number",
	FORMAT_INT("procedure_year") AS "procedure_year",
	"instance_date" AS "instance_date",
	FORMAT_INT("area_id") AS "area_id",
	FORMAT_INT("property_type_id") AS "property_type_id",
	FORMAT_INT("property_sub_type_id") AS "property_sub_type_id",
	FORMAT_VARCHAR("row_status_code") AS "row_status_code",
	FORMAT_FLOAT("procedure_area") AS "procedure_area",
	FORMAT_FLOAT("actual_area") AS "actual_area",
	FORMAT_FLOAT("property_total_value") AS "property_total_value",
	FORMAT_FLOAT("actual_worth") AS "actual_worth"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/ff09ccad-6047-4793-a776-9d282abb5cdb/resource/5921b912-d938-4d04-a4d1-a391b125a459/download/valuation.csv',
    'CSVWithNames'
);