INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_INT("authority_id") AS "authority_id",
	FORMAT_VARCHAR("commerce_registry_number") AS "commerce_registry_number",
	FORMAT_INT("chamber_commerce_number") AS "chamber_commerce_number",
	FORMAT_INT("ded_activity_code") AS "ded_activity_code",
	FORMAT_INT("parcel_id") AS "parcel_id",
	FORMAT_VARCHAR("rent_contract_no") AS "rent_contract_no",
	FORMAT_INT("participant_id") AS "participant_id",
	FORMAT_VARCHAR("license_number") AS "license_number",
	FORMAT_INT("status_id") AS "status_id",
	FORMAT_DATE_SLASH("issue_date") AS "issue_date",
	FORMAT_DATE_SLASH("expiry_date") AS "expiry_date",
	FORMAT_DATE_SLASH("cancel_date") AS "cancel_date",
	FORMAT_INT("legal_type_id") AS "legal_type_id",
	FORMAT_INT("activity_type_id") AS "activity_type_id",
	FORMAT_VARCHAR("trade_name_english") AS "trade_name_en",
	FORMAT_VARCHAR("trade_name_arabic") AS "trade_name_ar",
	FORMAT_VARCHAR("print_rmker_arabic") AS "print_rmker_ar"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/6f7f5f08-c633-4dae-b3ef-16f1ed54936d/resource/5749474d-c8da-4674-a002-f77fcfb34884/download/real_estate_licenses.csv',
    'CSVWithNames'
);