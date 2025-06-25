INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_INT("application_id") AS "application_id",
	FORMAT_INT("procedure_id") AS "procedure_id",
	FORMAT_INT("property_type_id") AS "property_type_id",
	FLOOR(REGEXP_REPLACE("request_id", '[^0-9]', '')::Nullable(Int128) / 1000) AS "request_id",
	FORMAT_INT("request_source_id") AS "request_source_id",
	"request_date" AS "request_date",
	FORMAT_INT("no_of_siteplans") AS "no_of_siteplans"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/9f7d502c-b93d-4603-bba5-02ccb6dcf017/resource/426cfbc5-206c-45fe-ab74-813352344811/download/map_requests.csv',
    'CSVWithNames'
);