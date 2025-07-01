CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    creation_date,
    parcel_number,
    property_number,
    master_project_id,
    project_id,
    building_name,
    building_number,
    bld_levels,
    floors,
    MAP_ROOMS_EN(rooms_id) AS rooms_type_english,
    MAP_ROOMS_AR(rooms_id) AS rooms_type_arabic,
    car_parks,
    elevators,
    swimming_pools,
    offices,
    shops,
    flats,
    built_up_area AS built_up_area_sqm,
    actual_area AS actual_area_sqm,
    common_area AS common_area_sqm,
    actual_common_area AS actual_common_area_sqm
FROM "{dld_database}"."{dld_table}_staging_clean"