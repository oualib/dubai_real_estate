CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    procedure_number,
    row_status_code,
    procedure_year,
    instance_date,
    area_id,
    property_type_id,
    property_sub_type_id,
    procedure_area,
    actual_area,
    property_total_value,
    actual_worth
FROM "{dld_database}"."{dld_table}_staging";