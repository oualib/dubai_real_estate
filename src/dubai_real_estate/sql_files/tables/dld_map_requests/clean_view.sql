CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    request_date,
    request_id,
    request_source_id,
    application_id,
    procedure_id,
    property_type_id,
    no_of_siteplans
FROM "{dld_database}"."{dld_table}_staging";