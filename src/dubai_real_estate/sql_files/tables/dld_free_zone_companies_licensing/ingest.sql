INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT 
	FORMAT_INT("fz_company_number") AS "fz_company_number",
	FORMAT_VARCHAR("fz_company_name_ar") AS "fz_company_name_ar",
	FORMAT_VARCHAR("fz_company_name_en") AS "fz_company_name_en",
	FORMAT_INT("license_source_id") AS "license_source_id",
	FORMAT_VARCHAR("license_number") AS "license_number",
	"license_issue_date" AS "license_issue_date",
	"license_expiry_date" AS "license_expiry_date",
	FORMAT_EMAIL("email") AS "email",
	FORMAT_WEBSITE("webpage") AS "webpage",
	FORMAT_PHONE_NUMBER("phone") AS "phone"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/6b5f31b1-e385-4435-bd9f-a16b2d11a6c0/resource/387a4596-ebca-4119-a419-d303a4898d08/download/free_zone_companies_licensing.csv',
    'CSVWithNames'
);