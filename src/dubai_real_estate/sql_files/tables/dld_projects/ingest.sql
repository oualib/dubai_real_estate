INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT
	FORMAT_INT("area_id") AS "area_id",
	FORMAT_INT("zoning_authority_id") AS "zoning_authority_id",
	FORMAT_INT("master_developer_id") AS "master_developer_id",
	FORMAT_INT("master_developer_number") AS "master_developer_number",
	FORMAT_VARCHAR("master_developer_name") AS "master_developer_name_ar",
	FORMAT_INT("developer_number") AS "developer_number",
	FORMAT_VARCHAR("developer_name") AS "developer_name_ar",
	FORMAT_INT("escrow_agent_id") AS "escrow_agent_id",
	FORMAT_INT("property_id") AS "property_id",
	FORMAT_VARCHAR("master_project_en") AS "master_project_en",
	FORMAT_VARCHAR("master_project_ar") AS "master_project_ar",
	FORMAT_INT("project_id") AS "project_id",
	FORMAT_INT("project_number") AS "project_number",
	FORMAT_VARCHAR("project_name") AS "project_name_ar",
	FORMAT_INT("project_type_id") AS "project_type_id",
	FORMAT_INT("project_classification_id") AS "project_classification_id",
	FORMAT_VARCHAR("project_status") AS "project_status_en",
	FORMAT_DATE("project_start_date") AS "project_start_date",
	FORMAT_DATE("project_end_date") AS "project_end_date",
	FORMAT_DATE("completion_date") AS "completion_date",
	FORMAT_DATE("cancellation_date") AS "cancellation_date",
	FORMAT_INT("percent_completed") AS "percent_completed",
	FORMAT_INT("no_of_lands") AS "no_of_lands",
	FORMAT_INT("no_of_buildings") AS "no_of_buildings",
	FORMAT_INT("no_of_villas") AS "no_of_villas",
	FORMAT_INT("no_of_units") AS "no_of_units",
	FORMAT_VARCHAR("project_description_en") AS "project_description_en",
	FORMAT_VARCHAR("project_description_ar") AS "project_description_ar"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/0b782e64-5950-4507-8f6e-02a0c30c7054/resource/db35b0cd-d291-4dde-b176-9b8d5765c7d9/download/projects.csv',
    'CSVWithNames'
);