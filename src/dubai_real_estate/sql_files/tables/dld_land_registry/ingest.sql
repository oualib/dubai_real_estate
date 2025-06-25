INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_INT("munc_number") AS "munc_number",
	FORMAT_INT("munc_zip_code") AS "munc_zip_code",
	FORMAT_INT("area_id") AS "area_id",
	FORMAT_INT("zone_id") AS "zone_id",
	FORMAT_INT("parcel_id") AS "parcel_id",
	FORMAT_INT("land_number") AS "land_number",
	FORMAT_INT("land_sub_number") AS "land_sub_number",
	FORMAT_INT("land_type_id") AS "land_type_id",
	FORMAT_INT("master_project_id") AS "master_project_id",
	FORMAT_VARCHAR("master_project_en") AS "master_project_en",
	FORMAT_VARCHAR("master_project_ar") AS "master_project_ar",
	FORMAT_INT("project_id") AS "project_id",
	FORMAT_VARCHAR("project_name_ar") AS "project_name_ar",
	FORMAT_VARCHAR("project_name_en") AS "project_name_en",
	FORMAT_INT("separated_from") AS "separated_from",
	FORMAT_INT("separated_reference") AS "separated_reference",
	FORMAT_INT("property_id") AS "property_id",
	FORMAT_INT("property_sub_type_id") AS "property_sub_type_id",
	FORMAT_BOOL("is_free_hold") AS "is_free_hold",
	FORMAT_BOOL("is_registered") AS "is_registered",
	FORMAT_VARCHAR("pre_registration_number") AS "pre_registration_number",
	FORMAT_FLOAT("actual_area") AS "actual_area"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/e4e01f57-6e07-469f-86c6-87a2d8a636b2/resource/02410e57-6979-4006-9143-d5088c9b79a3/download/land_registry.csv',
    'CSVWithNames'
);