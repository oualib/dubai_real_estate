CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
WITH
rent_map
AS
(
    SELECT
        contract_id,
        contract_reg_type_id,
        contract_start_date,
        contract_end_date,
        area_id,
        MAP_NEAREST_LANDMARK_REVERSE(nearest_landmark_en) AS nearest_landmark_id,
        MAP_NEAREST_METRO_REVERSE(nearest_metro_en) AS nearest_metro_id,
        MAP_NEAREST_MALL_REVERSE(nearest_mall_en) AS nearest_mall_id,
        property_type_id,
        ejari_property_type_id,
        MAP_PROPERTY_USAGE_REVERSE(property_usage_en) AS property_usage_id,
        master_project_en,
        project_name_en,
        is_free_hold,
        tenant_type_id,
        line_number,
        no_of_prop,
        MAP_ROOMS_REVERSE(rooms_en) AS rooms_id,
        actual_area,
        contract_amount,
        annual_amount
    FROM "{dld_database}"."{dld_table}_staging"
),
rent_projects_existing
AS
(
    SELECT
        *
    FROM rent_map
    WHERE 
        project_name_en IS NOT NULL
),
rent_master_projects_existing
AS
(
    SELECT
        *
    FROM rent_map
    WHERE 
        project_name_en IS NULL 
    AND master_project_en IS NOT NULL
),
rent_projects_missing
AS
(
    SELECT
        contract_id,
        contract_reg_type_id,
        contract_start_date,
        contract_end_date,
        area_id,
        nearest_landmark_id,
        nearest_metro_id,
        nearest_mall_id,
        property_type_id,
        ejari_property_type_id,
        property_usage_id,
        NULL::Nullable(Int128) AS master_project_id,
        NULL::Nullable(Int128) AS project_id,
        is_free_hold,
        tenant_type_id,
        line_number,
        no_of_prop,
        rooms_id,
        actual_area,
        contract_amount,
        annual_amount
    FROM rent_map
    WHERE 
        master_project_en IS NULL
    AND project_name_en IS NULL
),
rent_projects_id_in 
AS
(
    SELECT
        p0.contract_id,
        p0.contract_reg_type_id,
        p0.contract_start_date,
        p0.contract_end_date,
        p0.area_id,
        p0.nearest_landmark_id,
        p0.nearest_metro_id,
        p0.nearest_mall_id,
        p0.property_type_id,
        p0.ejari_property_type_id,
        p0.property_usage_id,
        p1.master_project_id,
        p1.project_id,
        p0.is_free_hold,
        p0.tenant_type_id,
        p0.line_number,
        p0.no_of_prop,
        p0.rooms_id,
        p0.actual_area,
        p0.contract_amount,
        p0.annual_amount
    FROM 
        rent_projects_existing AS p0
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
rent_master_projects_id_in 
AS
(
    SELECT
        p0.contract_id,
        p0.contract_reg_type_id,
        p0.contract_start_date,
        p0.contract_end_date,
        p0.area_id,
        p0.nearest_landmark_id,
        p0.nearest_metro_id,
        p0.nearest_mall_id,
        p0.property_type_id,
        p0.ejari_property_type_id,
        p0.property_usage_id,
        p1.master_project_id,
        NULL::Nullable(Int128) AS project_id,
        p0.is_free_hold,
        p0.tenant_type_id,
        p0.line_number,
        p0.no_of_prop,
        p0.rooms_id,
        p0.actual_area,
        p0.contract_amount,
        p0.annual_amount
    FROM 
    rent_master_projects_existing AS p0
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
rent_projects_id
AS
(
    SELECT * FROM
    (
        SELECT * FROM rent_projects_id_in
        UNION ALL
        SELECT * FROM rent_master_projects_id_in
        UNION ALL
        SELECT * FROM rent_projects_missing
    ) AS p0
),
rent_clean
AS
(
    SELECT
        contract_id,
        contract_reg_type_id,
        contract_start_date,
        contract_end_date,
        area_id,
        nearest_landmark_id,
        nearest_metro_id,
        nearest_mall_id,
        property_type_id,
        ejari_property_type_id,
        property_usage_id,
        master_project_id,
        project_id,
        is_free_hold,
        tenant_type_id,
        line_number,
        no_of_prop,
        rooms_id,
        actual_area,
        contract_amount,
        annual_amount
    FROM rent_projects_id
)
SELECT * FROM rent_clean;