CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    creation_date,
    COALESCE(parcel_id, property_id) AS parcel_number,
    grandparent_property_id AS property_number,
    NULLIFNEG(master_project_id) AS master_project_id,
    NULLIFNEG(project_id) AS project_id,
    building_number,
    unit_number,
    floor,
    MAP_ROOMS_REVERSE(rooms_en) AS rooms_id,
    unit_parking_number,
    parking_allocation_type AS parking_allocation_type_id,
    actual_area,
    common_area,
    actual_common_area,
    unit_balcony_area
FROM "{dld_database}"."{dld_table}_staging";