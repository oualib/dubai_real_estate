INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_INT("main_office_id") AS "main_office_id",
	FORMAT_BOOL("is_branch") AS "is_branch",
	FORMAT_INT("real_estate_number") AS "real_estate_number",
	FORMAT_INT("participant_id") AS "participant_id",
	FORMAT_INT("activity_type_id") AS "activity_type_id",
	FORMAT_INT("license_source_id") AS "license_source_id",
	FORMAT_VARCHAR("license_number") AS "license_number",
	FORMAT_DATE("license_issue_date") AS "license_issue_date",
	FORMAT_DATE("license_expiry_date") AS "license_expiry_date",
	FIRST_EN(FORMAT_NAME("webpage"), NULL, NULL) AS "contact_name_en",
	FIRST_AR(FORMAT_NAME("webpage"), NULL, NULL) AS "contact_name_ar",
	COALESCE(FORMAT_WEBSITE("webpage"), FORMAT_EMAIL("webpage")) AS "contact",
	FORMAT_PHONE_NUMBER("webpage") AS "mobile",
	COALESCE(FORMAT_PHONE_NUMBER("webpage"), FORMAT_PHONE_NUMBER("phone")) AS "phone",
	FORMAT_PHONE_NUMBER("fax") AS "fax"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/fcf32825-ad42-4fe8-a779-e0b116485175/resource/05617ecd-1e9a-4ad4-b32a-139a6b0f7dff/download/offices.csv',
    'CSVWithNames'
);