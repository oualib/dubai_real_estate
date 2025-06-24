INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_VARCHAR("location"),
	FORMAT_INT("parent_permit_id"),
	FORMAT_INT("parent_service_id"),
	FORMAT_INT("permit_id"),
	FORMAT_INT("service_id"),
	FORMAT_INT("permit_status_id"),
	FORMAT_DATE("start_date"),
	FORMAT_DATE("end_date"),
	FORMAT_VARCHAR("license_number"),
	FORMAT_VARCHAR("exhibition_name_en"),
	FORMAT_VARCHAR("exhibition_name_ar"),
	FORMAT_NAME("participant_name_en"),
	FORMAT_NAME("participant_name_ar")
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/1e28d7b9-d85a-4832-bd89-59cb79c6cd72/resource/44b2d189-bdb7-4200-959f-f065977093bb/download/real_estate_permits.csv',
    'CSVWithNames'
);