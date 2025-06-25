CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    request_date,
    request_id,
    MAP_REQUEST_SOURCE_EN(request_source_id) AS request_source_name_english,
    MAP_REQUEST_SOURCE_AR(request_source_id) AS request_source_name_arabic,
    MAP_APPLICATION_EN(application_id) AS application_name_english,
    MAP_APPLICATION_AR(application_id) AS application_name_arabic,
    MAP_PROCEDURE_EN(procedure_id) AS procedure_name_english,
    MAP_PROCEDURE_AR(procedure_id) AS procedure_name_arabic,
    MAP_PROPERTY_TYPE_EN(property_type_id) AS property_type_english,
    MAP_PROPERTY_TYPE_AR(property_type_id) AS property_type_arabic,
    no_of_siteplans
FROM "{dld_database}"."{dld_table}_staging_clean"