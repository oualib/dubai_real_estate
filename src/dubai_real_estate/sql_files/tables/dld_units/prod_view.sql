CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    creation_date,
    parcel_number,
    property_number,
    master_project_id,
    project_id,
    building_number,
    unit_number,
    floor,
    MAP_ROOMS_EN(rooms_id) AS rooms_type_english,
    MAP_ROOMS_AR(rooms_id) AS rooms_type_arabic,
    unit_parking_number,
    MAP_PARKING_ALLOCATION_TYPE_EN(parking_allocation_type_id) AS parking_allocation_type_english,
    MAP_PARKING_ALLOCATION_TYPE_AR(parking_allocation_type_id) AS parking_allocation_type_arabic,
    actual_area AS actual_area_sqm,
    common_area AS common_area_sqm,
    actual_common_area AS actual_common_area_sqm,
    unit_balcony_area AS unit_balcony_area_sqm
FROM "{dld_database}"."{dld_table}_staging_clean"