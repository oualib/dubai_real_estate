CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
WITH
transactions_map
AS
(
    SELECT
        transaction_id,
        trans_group_id,
        procedure_id,
        instance_date,
        area_id,
        MAP_NEAREST_LANDMARK_REVERSE(nearest_landmark_en) AS nearest_landmark_id,
        MAP_NEAREST_METRO_REVERSE(nearest_metro_en) AS nearest_metro_id,
        MAP_NEAREST_MALL_REVERSE(nearest_mall_en) AS nearest_mall_id,
        property_type_id,
        property_sub_type_id,
        MAP_PROPERTY_USAGE_REVERSE(property_usage_en) AS property_usage_id,
        reg_type_id,
        master_project_en,
        project_name_en,
        building_name_en,
        building_name_ar,
        MAP_ROOMS_REVERSE(rooms_en) AS rooms_id,
        has_parking,
        procedure_area, 
        actual_worth,
        no_of_parties_role_1,
        no_of_parties_role_2,
        no_of_parties_role_3
    FROM "{dld_database}"."{dld_table}_staging"
),
transactions_projects_existing
AS
(
    SELECT
        *
    FROM transactions_map
    WHERE 
        project_name_en IS NOT NULL
),
transactions_master_projects_existing
AS
(
    SELECT
        *
    FROM transactions_map
    WHERE 
        project_name_en IS NULL 
    AND master_project_en IS NOT NULL
),
transactions_projects_missing
AS
(
    SELECT
        transaction_id,
        trans_group_id,
        procedure_id,
        instance_date,
        area_id,
        nearest_landmark_id,
        nearest_metro_id,
        nearest_mall_id,
        property_type_id,
        property_sub_type_id,
        property_usage_id,
        reg_type_id,
        NULL::Nullable(Int128) AS master_project_id,
        NULL::Nullable(Int128) AS project_id,
        building_name_en,
        building_name_ar,
        rooms_id,
        has_parking,
        procedure_area, 
        actual_worth,
        no_of_parties_role_1,
        no_of_parties_role_2,
        no_of_parties_role_3
    FROM transactions_map
    WHERE 
        master_project_en IS NULL
    AND project_name_en IS NULL
),
transactions_projects_id_in 
AS
(
    SELECT
        p0.transaction_id,
        p0.trans_group_id,
        p0.procedure_id,
        p0.instance_date,
        p0.area_id,
        p0.nearest_landmark_id,
        p0.nearest_metro_id,
        p0.nearest_mall_id,
        p0.property_type_id,
        p0.property_sub_type_id,
        p0.property_usage_id,
        p0.reg_type_id,
        p1.master_project_id,
        p1.project_id,
        p0.building_name_en,
        p0.building_name_ar,
        p0.rooms_id,
        p0.has_parking,
        p0.procedure_area, 
        p0.actual_worth,
        p0.no_of_parties_role_1,
        p0.no_of_parties_role_2,
        p0.no_of_parties_role_3
    FROM 
    transactions_projects_existing AS p0
    LEFT JOIN
    (
        SELECT
            project_name_en,
            master_project_id,
            project_id
        FROM
        (
            SELECT
                project_name_en,
                master_project_id,
                project_id,
                ROW_NUMBER() OVER (PARTITION BY project_name_en ORDER BY cnt_project DESC) AS row_nb
            FROM
            (
                SELECT
                    project_name_en,
                    master_project_id,
                    project_id,
                    COUNT(*) OVER (PARTITION BY project_id) AS cnt_project
                FROM
                "{dld_database}"."{projects}_staging_clean"
                WHERE project_name_en IS NOT NULL
            ) AS q0
        ) AS q1
        WHERE row_nb = 1
    ) AS p1
    USING (project_name_en)
),
transactions_master_projects_id_in 
AS
(
    SELECT
        p0.transaction_id,
        p0.trans_group_id,
        p0.procedure_id,
        p0.instance_date,
        p0.area_id,
        p0.nearest_landmark_id,
        p0.nearest_metro_id,
        p0.nearest_mall_id,
        p0.property_type_id,
        p0.property_sub_type_id,
        p0.property_usage_id,
        p0.reg_type_id,
        p1.master_project_id,
        NULL::Nullable(Int128) AS project_id,
        p0.building_name_en,
        p0.building_name_ar,
        p0.rooms_id,
        p0.has_parking,
        p0.procedure_area, 
        p0.actual_worth,
        p0.no_of_parties_role_1,
        p0.no_of_parties_role_2,
        p0.no_of_parties_role_3
    FROM 
    transactions_master_projects_existing AS p0
    LEFT JOIN
    (
        SELECT
             master_project_id,
             master_project_en
        FROM
        (
            SELECT
                 master_project_id,
                 master_project_en,
                 ROW_NUMBER() OVER (PARTITION BY master_project_en ORDER BY total DESC) AS row_nb,
                 total
            FROM
            (
                SELECT
                    master_project_en,
                    master_project_id,
                    COUNT(*) AS total
                FROM
                    "{dld_database}"."{projects}_staging_clean"
                GROUP BY master_project_en, master_project_id
            ) AS q0
        ) AS q1
        WHERE row_nb = 1
          AND master_project_id IS NOT NULL
          AND master_project_en IS NOT NULL
    ) AS p1
    USING(master_project_en)
),
transactions_projects_id
AS
(
    SELECT * FROM
    (
        SELECT * FROM transactions_projects_id_in
        UNION ALL
        SELECT * FROM transactions_master_projects_id_in
        UNION ALL
        SELECT * FROM transactions_projects_missing
    ) AS p0
),
transactions_clean
AS
(
    SELECT
        transaction_id,
        trans_group_id,
        procedure_id,
        CASE 
            WHEN YEAR(instance_date) > 1970 
                THEN instance_date
            WHEN instance_date IS NULL
                THEN NULL
            ELSE (splitByChar('-', transaction_id::Varchar(60))[3] || '-' || formatDateTime(instance_date, '%m-%d'))::Nullable(Date)
        END AS instance_date,
        area_id,
        nearest_landmark_id,
        nearest_metro_id,
        nearest_mall_id,
        master_project_id,
        project_id,
        TRIM(UPPER(building_name_en)) AS building_name,
        FORMAT_INT(REGEXP_REPLACE(building_name_en, '[^0-9]', '')) AS building_number,
        property_type_id,
        property_sub_type_id,
        property_usage_id,
        reg_type_id,
        no_of_parties_role_1,
        no_of_parties_role_2,
        no_of_parties_role_3,
        has_parking,
        rooms_id,
        procedure_area,
        actual_worth
    FROM transactions_projects_id
)
SELECT * FROM transactions_clean;