CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
WITH
parcel_missing AS
(
SELECT 
    parcel_number,
    MIN(munc_number) AS munc_number,
    MIN(munc_zip_code) AS munc_zip_code,
    area_id,
    zone_id,
    MIN(land_number) AS land_number,
    MIN(land_sub_number) AS land_sub_number,
    MIN(land_type_id) AS land_type_id,
    MIN(NULLIFNEG(master_project_id)) AS master_project_id,
    MIN(NULLIFNEG(project_id)) AS project_id,
    separated_from,
    separated_reference,
    MIN(property_id) AS property_id,
    MIN(property_sub_type_id) AS property_sub_type_id,
    groupBitOr(is_free_hold) AS is_free_hold,
    groupBitOr(is_registered) AS is_registered,
    groupArray(pre_registration_number) AS pre_registration_number,
    MIN(actual_area) AS actual_area,
    MIN(creation_date) AS creation_date
FROM
    (
        SELECT
            COALESCE(parcel_id, property_id) AS parcel_number,
            NULL::Nullable(Int128) AS munc_number,
            NULL::Nullable(Int128) AS munc_zip_code,
            area_id,
            zone_id,
            land_number,
            land_sub_number,
            land_type_id,
            master_project_id,
            project_id,
            NULL::Nullable(Int128) AS separated_from,
            NULL::Nullable(Int128) AS separated_reference,
            property_id,
            property_sub_type_id,
            is_free_hold,
            is_registered,
            pre_registration_number,
            built_up_area * 0.092903 AS actual_area,
            creation_date
        FROM "{dld_database}"."{buildings}_staging" WHERE parcel_id IS NULL
        UNION DISTINCT
        SELECT
            COALESCE(parcel_id, property_id) AS parcel_number,
            munc_number,
            munc_zip_code,
            area_id,
            zone_id,
            land_number,
            land_sub_number,
            land_type_id,
            master_project_id,
            project_id,
            NULL::Nullable(Int128) AS separated_from,
            NULL::Nullable(Int128) AS separated_reference,
            property_id,
            property_sub_type_id,
            is_free_hold,
            is_registered,
            pre_registration_number,
            SUM(actual_area) OVER (PARTITION BY parcel_id, project_name_en) * 0.092903 AS actual_area,
            creation_date
        FROM "{dld_database}"."{units}_staging" WHERE parcel_id IS NULL
    ) AS q0
    GROUP BY ALL
),
parcel_existing AS
(
SELECT 
    parcel_number,
    MIN(munc_number) AS munc_number,
    MIN(munc_zip_code) AS munc_zip_code,
    area_id,
    zone_id,
    MIN(land_number) AS land_number,
    MIN(land_sub_number) AS land_sub_number,
    MIN(land_type_id) AS land_type_id,
    MIN(NULLIFNEG(master_project_id)) AS master_project_id,
    MIN(NULLIFNEG(project_id)) AS project_id,
    separated_from,
    separated_reference,
    MIN(property_id) AS property_id,
    MIN(property_sub_type_id) AS property_sub_type_id,
    groupBitOr(is_free_hold) AS is_free_hold,
    groupBitOr(is_registered) AS is_registered,
    groupArray(pre_registration_number) AS pre_registration_number,
    MIN(actual_area) AS actual_area,
    MIN(creation_date) AS creation_date
FROM
    (
        SELECT
            COALESCE(parcel_id, property_id) AS parcel_number,
            NULL::Nullable(Int128) AS munc_number,
            NULL::Nullable(Int128) AS munc_zip_code,
            area_id,
            zone_id,
            land_number,
            land_sub_number,
            land_type_id,
            master_project_id,
            project_id,
            NULL::Nullable(Int128) AS separated_from,
            NULL::Nullable(Int128) AS separated_reference,
            property_id,
            property_sub_type_id,
            is_free_hold,
            is_registered,
            pre_registration_number,
            built_up_area * 0.092903 AS actual_area,
            creation_date
        FROM "{dld_database}"."{buildings}_staging"
        UNION DISTINCT
        SELECT
            COALESCE(parcel_id, property_id) AS parcel_number,
            munc_number,
            munc_zip_code,
            area_id,
            zone_id,
            land_number,
            land_sub_number,
            land_type_id,
            master_project_id,
            project_id,
            NULL::Nullable(Int128) AS separated_from,
            NULL::Nullable(Int128) AS separated_reference,
            property_id,
            property_sub_type_id,
            is_free_hold,
            is_registered,
            pre_registration_number,
            SUM(actual_area) OVER (PARTITION BY parcel_id, project_name_en) * 0.092903 AS actual_area,
            creation_date
        FROM "{dld_database}"."{units}_staging"
    ) AS q0
    GROUP BY ALL
),
land_registry AS
(
    SELECT
        COALESCE(parcel_id, property_id) AS parcel_number,
        MIN(munc_number) AS munc_number,
        MIN(munc_zip_code) AS munc_zip_code,
        area_id,
        zone_id,
        MIN(land_number) AS land_number,
        MIN(land_sub_number) AS land_sub_number,
        MIN(land_type_id) AS land_type_id,
        MIN(master_project_id) AS master_project_id,
        MIN(NULLIFNEG(project_id)) AS project_id,
        MIN(separated_from) AS separated_from,
        MIN(separated_reference) AS separated_reference,
        MIN(property_id) AS property_id,
        MIN(property_sub_type_id) AS property_sub_type_id,
        groupBitOr(is_free_hold) AS is_free_hold,
        groupBitOr(is_registered) AS is_registered,
        groupArray(pre_registration_number) AS pre_registration_number,
        MAX(actual_area) AS actual_area,
        NULL::Nullable(Date) AS creation_date
    FROM "{dld_database}"."{dld_table}_staging"
    GROUP BY ALL
),
land_clean AS
(
    SELECT
        creation_date,
        parcel_number,
        munc_number,
        munc_zip_code,
        area_id,
        zone_id,
        property_id AS land_property_number,
        separated_from AS land_separated_from,
        separated_reference AS land_separated_reference,
        land_number,
        land_sub_number,
        land_type_id,
        master_project_id,
        project_id,
        property_sub_type_id,
        is_free_hold,
        is_registered,
        pre_registration_number,
        actual_area
    FROM
    (
        SELECT 
            *
        FROM 
        (
            SELECT
                COALESCE(p1.parcel_number, p0.parcel_number) AS parcel_number,
                COALESCE(p0.munc_number, p1.munc_number) AS munc_number,
                COALESCE(p0.munc_zip_code, p1.munc_zip_code) AS munc_zip_code,
                COALESCE(p0.area_id, p1.area_id) AS area_id,
                COALESCE(p0.zone_id, p1.zone_id) AS zone_id,
                COALESCE(p0.land_number, p1.land_number) AS land_number,
                COALESCE(p0.land_sub_number, p1.land_sub_number) AS land_sub_number,
                COALESCE(p0.land_type_id, p1.land_type_id) AS land_type_id,
                COALESCE(p0.master_project_id, p1.master_project_id) AS master_project_id,
                COALESCE(p0.project_id, p1.project_id) AS project_id,
                COALESCE(p0.separated_from, p1.separated_from) AS separated_from,
                COALESCE(p0.separated_reference, p1.separated_reference) AS separated_reference,
                COALESCE(p0.property_id, p1.property_id) AS property_id,
                COALESCE(p0.property_sub_type_id, p1.property_sub_type_id) AS property_sub_type_id,
                COALESCE(p0.is_free_hold, p1.is_free_hold) AS is_free_hold,
                COALESCE(p0.is_registered, p1.is_registered) AS is_registered,
                COALESCE(p0.pre_registration_number, p1.pre_registration_number) AS pre_registration_number,
                COALESCE(p0.actual_area, p1.actual_area) AS actual_area,
                COALESCE(p0.creation_date, p1.creation_date) AS creation_date
            FROM 
            land_registry AS p0
            LEFT JOIN
            parcel_existing AS p1
            USING (parcel_number)
        ) AS q0
        UNION DISTINCT
        SELECT * FROM parcel_missing
    ) AS q1
    ORDER BY creation_date, parcel_number
)
SELECT * FROM land_clean;