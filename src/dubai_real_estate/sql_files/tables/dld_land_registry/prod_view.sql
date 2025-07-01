CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    creation_date,
    parcel_number,
    munc_number,
    munc_zip_code,
    MAP_AREA_NAME_EN(area_id) AS area_name_english,
    MAP_AREA_NAME_AR(area_id) AS area_name_arabic,
    land_property_number,
    land_separated_from,
    land_separated_reference,
    land_number,
    land_sub_number,
    MAP_LAND_TYPE_EN(land_type_id) AS land_type_english,
    MAP_LAND_TYPE_AR(land_type_id) AS land_type_arabic,
    master_project_id,
    project_id,
    MAP_PROPERTY_SUB_TYPE_EN(property_sub_type_id) AS property_sub_type_english,
    MAP_PROPERTY_SUB_TYPE_AR(property_sub_type_id) AS property_sub_type_arabic,
    is_free_hold,
    is_registered,
    pre_registration_number,
    actual_area AS actual_area_sqm
FROM "{dld_database}"."{dld_table}_staging_clean"