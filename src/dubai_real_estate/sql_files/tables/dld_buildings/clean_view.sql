CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    creation_date,
    parcel_number,
    property_number,
    master_project_id,
    project_id,
    building_name,
    building_number_final AS building_number,
    bld_levels,
    floors,
    rooms_id,
    car_parks,
    elevators,
    swimming_pools,
    offices,
    shops,
    flats,
    built_up_area,
    actual_area,
    common_area,
    actual_common_area
FROM
(
    SELECT 
        creation_date,
        COALESCE(parcel_id, property_id) AS parcel_number,
        parent_property_id AS property_number,
        NULLIFNEG(master_project_id) AS master_project_id,
        NULLIFNEG(project_id) AS project_id,
        TRIM(UPPER(building_number)) AS building_name,
        FORMAT_INT(REGEXP_REPLACE(building_number, '[^0-9]', '')) AS building_number_final,
        bld_levels,
        floors,
        MAP_ROOMS_REVERSE(rooms_en) AS rooms_id,
        car_parks,
        elevators,
        swimming_pools,
        offices,
        shops,
        flats,
        built_up_area,
        actual_area,
        common_area,
        actual_common_area
    FROM "{dld_database}"."{dld_table}_staging"
) dld_building_clean_final;