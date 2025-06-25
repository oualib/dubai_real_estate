CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    procedure_number,
    row_status_code,
    procedure_year,
    instance_date,
    MAP_AREA_NAME_EN(area_id) AS area_name_english,
    MAP_AREA_NAME_AR(area_id) AS area_name_arabic,
    MAP_PROPERTY_TYPE_EN(property_type_id) AS property_type_english,
    MAP_PROPERTY_TYPE_AR(property_type_id) AS property_type_arabic,
    MAP_PROPERTY_SUB_TYPE_EN(property_sub_type_id) AS property_sub_type_english,
    MAP_PROPERTY_SUB_TYPE_AR(property_sub_type_id) AS property_sub_type_arabic,
    procedure_area,
    actual_area,
    property_total_value,
    actual_worth
FROM "{dld_database}"."{dld_table}_staging_clean"