INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_VARCHAR("company_name_en") AS "company_name_en",
	FORMAT_VARCHAR("company_name_ar") AS "company_name_ar",
	FORMAT_PHONE_NUMBER("phone") AS "phone",
	FORMAT_EMAIL("email") AS "email",
	FORMAT_FLOAT("latitude") AS "latitude",
	FORMAT_FLOAT("longitude") AS "longitude"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/83e36ed4-adde-4a5f-aad2-5ac990b87d12/resource/dbc2bbd6-a2ba-4963-ae3c-fccaf14f618f/download/licenced_owner_associations.csv',
    'CSVWithNames'
);