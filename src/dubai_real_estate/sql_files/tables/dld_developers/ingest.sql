INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT 
	FORMAT_INT("participant_id") AS "participant_id",
	FORMAT_INT("developer_number") AS "developer_number",
	FIRST_AR(FORMAT_NAME("developer_name_ar"), FORMAT_NAME("webpage"), FORMAT_NAME("developer_name_en")) AS "developer_name_ar_final",
	FIRST_EN(FORMAT_NAME("developer_name_en"), FORMAT_NAME("webpage"), FORMAT_NAME("developer_name_ar")) AS "developer_name_en_final",
	FORMAT_INT("chamber_of_commerce_no") AS "chamber_commerce_number",
	FORMAT_DATE("registration_date") AS "registration_date",
	NULLIFNEGS(FORMAT_INT("legal_status")) AS "legal_status",
	FORMAT_INT("license_source_id") AS "license_source_id", -- TODO: VERIFY
	NULLIFNEGS(FORMAT_INT("license_type_id")) AS "license_type_id",
	FORMAT_VARCHAR("license_number") AS "license_number_final",
	FORMAT_DATE("license_issue_date") AS "license_issue_date",
	FORMAT_DATE("license_expiry_date") AS "license_expiry_date",
	COALESCE(FORMAT_WEBSITE("webpage"), FORMAT_EMAIL("webpage")) AS "contact",
	FORMAT_PHONE_NUMBER("phone") AS "phone",
	FORMAT_PHONE_NUMBER("fax") AS "fax"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/ac68c7d5-8acb-441c-9a7d-6e6d72942d86/resource/57ca3b1a-775d-4f6c-8b04-19e02f6b4a03/download/developers.csv',
    'CSVWithNames'
);