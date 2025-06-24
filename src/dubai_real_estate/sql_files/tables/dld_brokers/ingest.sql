INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT 
	FORMAT_INT("real_estate_number") AS "real_estate_number",
	FORMAT_INT("participant_id") AS "participant_id",
	FORMAT_INT("broker_number") AS "broker_number",
	FIRST_AR(FORMAT_NAME("broker_name_ar"), FORMAT_NAME("broker_name_en"), NULL) AS "broker_name_ar_final",
	FIRST_EN(FORMAT_NAME("broker_name_en"), FORMAT_NAME("broker_name_ar"), NULL) AS "broker_name_en_final",
	FORMAT_DATE("license_start_date") AS "license_start_date",
	"license_end_date" AS "license_end_date",
	FORMAT_BOOL("gender") AS "is_female",
	COALESCE(FORMAT_WEBSITE("webpage"), FORMAT_EMAIL("webpage"), FORMAT_NAME("webpage")) AS "contact",
	COALESCE(FORMAT_PHONE_NUMBER("phone"), FORMAT_PHONE_NUMBER("webpage")) AS "phone"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/4830ea7f-0a2b-4192-bb21-4002bcdb01ec/resource/84897e8a-1c2f-43df-8e55-bea205a8a66e/download/brokers.csv',
    'CSVWithNames'
);