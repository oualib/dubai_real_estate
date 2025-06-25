CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
WITH 
projects_units_missing AS
(
SELECT
    area_id,
    NULL::Nullable(Int128) AS zoning_authority_id,
    NULL::Nullable(Int128) AS master_developer_number,
    NULL::Nullable(Int128) AS developer_number,
    NULL::Nullable(Int128) AS escrow_agent_id,
    NULL::Nullable(Int128) AS property_id,
    master_project_id,
    master_project_en, 
    master_project_ar,
    project_id,
    project_id AS project_number,
    project_name_en,
    project_name_ar,
    NULL::Nullable(Int128) AS project_type_id,
    NULL::Nullable(Int128) AS project_classification_id,
    NULL::Nullable(Int128) AS project_status_id,
    project_start_date,
    NULL::Nullable(Date) AS project_end_date,
    NULL::Nullable(Date) AS completion_date,
    NULL::Nullable(Date) AS cancellation_date,
    NULL::Nullable(Int128) AS percent_completed,
    NULL::Nullable(Int128) AS no_of_lands,
    NULL::Nullable(Int128) AS no_of_buildings,
    NULL::Nullable(Int128) AS no_of_villas,
    no_of_units::Nullable(Int128),
    NULL::Nullable(Varchar) AS project_description_en,
    NULL::Nullable(Varchar) AS project_description_ar
FROM
(
    SELECT * FROM
    (
        SELECT 
            MIN(area_id) OVER (PARTITION BY project_id) AS area_id,
            MIN(NULLIFNEGS(master_project_id)) OVER (PARTITION BY project_id) AS master_project_id,
            LAST_VALUE(master_project_en) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_en,
            LAST_VALUE(master_project_ar) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_ar,
            project_id,
            project_name_en,
            project_name_ar,
            MAX(creation_date) OVER (PARTITION BY project_id) AS project_start_date,
            COUNT(*) OVER (PARTITION BY project_id) AS no_of_units
        FROM 
            "{dld_database}"."{units}_staging"
        WHERE project_id NOT IN (SELECT DISTINCT project_id FROM "{dld_database}"."{dld_table}_staging")
    ) AS q0
    GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9
) AS q1
),
projects_units_existing AS
(
SELECT
    area_id,
    NULL::Nullable(Int128) AS zoning_authority_id,
    NULL::Nullable(Int128) AS master_developer_number,
    NULL::Nullable(Int128) AS developer_number,
    NULL::Nullable(Int128) AS escrow_agent_id,
    NULL::Nullable(Int128) AS property_id,
    master_project_id,
    master_project_en, 
    master_project_ar,
    project_id,
    project_id AS project_number,
    project_name_en,
    project_name_ar,
    NULL::Nullable(Int128) AS project_type_id,
    NULL::Nullable(Int128) AS project_classification_id,
    NULL::Nullable(Int128) AS project_status_id,
    project_start_date,
    NULL::Nullable(Date) AS project_end_date,
    NULL::Nullable(Date) AS completion_date,
    NULL::Nullable(Date) AS cancellation_date,
    NULL::Nullable(Int128) AS percent_completed,
    NULL::Nullable(Int128) AS no_of_lands,
    NULL::Nullable(Int128) AS no_of_buildings,
    NULL::Nullable(Int128) AS no_of_villas,
    no_of_units::Nullable(Int128) AS no_of_units,
    NULL::Nullable(Varchar) AS project_description_en,
    NULL::Nullable(Varchar) AS project_description_ar
FROM
(
    SELECT * FROM
    (
        SELECT 
            MIN(area_id) OVER (PARTITION BY project_id) AS area_id,
            MIN(NULLIFNEGS(master_project_id)) OVER (PARTITION BY project_id) AS master_project_id,
            LAST_VALUE(master_project_en) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_en,
            LAST_VALUE(master_project_ar) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_ar,
            project_id,
            project_name_en,
            project_name_ar,
            MAX(creation_date) OVER (PARTITION BY project_id) AS project_start_date,
            COUNT(*) OVER (PARTITION BY project_id) AS no_of_units
        FROM 
            "{dld_database}"."{units}_staging"
        WHERE project_id IN (SELECT DISTINCT project_id FROM "{dld_database}"."{dld_table}_staging")
    ) AS q0
    GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9
) AS q1
),
projects AS
(
SELECT
    area_id,
    zoning_authority_id,
    master_developer_number,
    developer_number,
    escrow_agent_id,
    property_id,
    NULL::Nullable(Int128) AS master_project_id,
    master_project_en, 
    master_project_ar,
    project_id,
    project_id AS project_number,
    NULL::Nullable(Varchar) AS project_name_en,
    project_name_ar,
    project_type_id,
    project_classification_id,
    MAP_PROJECT_STATUS_REVERSE(project_status_en) AS project_status_id,
    project_start_date,
    project_end_date,
    completion_date,
    cancellation_date,
    percent_completed,
    no_of_lands,
    no_of_buildings,
    no_of_villas,
    no_of_units,
    project_description_en,
    project_description_ar
FROM
    "{dld_database}"."{dld_table}_staging"
),
projects_clean_units AS
(
    SELECT 
        *
    FROM
    (
        SELECT 
            *
        FROM
        (
            SELECT 
                COALESCE(p0.area_id::Nullable(Int128), p1.area_id::Nullable(Int128)) AS area_id,
                COALESCE(p0.zoning_authority_id::Nullable(Int128), p1.zoning_authority_id::Nullable(Int128)) AS zoning_authority_id,
                COALESCE(p0.master_developer_number::Nullable(Int128), p1.master_developer_number::Nullable(Int128)) AS master_developer_number,
                COALESCE(p0.developer_number::Nullable(Int128), p1.developer_number::Nullable(Int128)) AS developer_number,
                COALESCE(p0.escrow_agent_id::Nullable(Int128), p1.escrow_agent_id::Nullable(Int128)) AS escrow_agent_id,
                COALESCE(p0.property_id::Nullable(Int128), p1.property_id::Nullable(Int128)) AS property_id,
                COALESCE(p0.master_project_id::Nullable(Int128), p1.master_project_id::Nullable(Int128)) AS master_project_id,
                COALESCE(p0.master_project_en,  p1.master_project_en) AS master_project_en,
                COALESCE(p0.master_project_ar, p1.master_project_ar) AS master_project_ar,
                COALESCE(p0.project_id::Nullable(Int128), p1.project_id::Nullable(Int128)) AS project_id,
                COALESCE(p0.project_number::Nullable(Int128), p1.project_number::Nullable(Int128)) AS project_number,
                COALESCE(p0.project_name_en, p1.project_name_en) AS project_name_en,
                COALESCE(p0.project_name_ar, p1.project_name_ar) AS project_name_ar,
                COALESCE(p0.project_type_id::Nullable(Int128), p1.project_type_id::Nullable(Int128)) AS project_type_id,
                COALESCE(p0.project_classification_id::Nullable(Int128), p1.project_classification_id::Nullable(Int128)) AS project_classification_id,
                COALESCE(p0.project_status_id::Nullable(Int128), p1.project_status_id::Nullable(Int128)) AS project_status_id,
                COALESCE(p0.project_start_date, p1.project_start_date) AS project_start_date,
                COALESCE(p0.project_end_date, p1.project_end_date) AS project_end_date,
                COALESCE(p0.completion_date, p1.completion_date) AS completion_date,
                COALESCE(p0.cancellation_date, p1.cancellation_date) AS cancellation_date,
                COALESCE(p0.percent_completed::Nullable(Int128), p1.percent_completed::Nullable(Int128)) AS percent_completed,
                COALESCE(p0.no_of_lands::Nullable(Int128), p1.no_of_lands::Nullable(Int128)) AS no_of_lands,
                COALESCE(p0.no_of_buildings::Nullable(Int128), p1.no_of_buildings::Nullable(Int128)) AS no_of_buildings,
                COALESCE(p0.no_of_villas::Nullable(Int128), p1.no_of_villas::Nullable(Int128)) AS no_of_villas,
                COALESCE(p0.no_of_units::Nullable(Int128), p1.no_of_units::Nullable(Int128)) AS no_of_units,
                COALESCE(p0.project_description_en, p1.project_description_en) AS project_description_en,
                COALESCE(p0.project_description_ar, p1.project_description_ar) AS project_description_ar
            FROM 
            projects AS p0
            LEFT JOIN
            projects_units_existing AS p1
            USING(project_id)
        ) AS q0
        UNION ALL
        SELECT * FROM projects_units_missing
    ) AS q1
),
projects_land_missing AS
(
    SELECT
        area_id, 
        NULL::Nullable(Int128) AS zoning_authority_id,
        NULL::Nullable(Int128) AS master_developer_number,
        NULL::Nullable(Int128) AS developer_number,
        NULL::Nullable(Int128) AS escrow_agent_id,
        property_id,
        master_project_id,
        master_project_en,
        master_project_ar,
        project_id,
        project_id AS project_number,
        project_name_en,
        project_name_ar,
        NULL::Nullable(Int128) AS project_type_id,
        NULL::Nullable(Int128) AS project_classification_id,
        NULL::Nullable(Int128) AS project_status_id,
        NULL::Nullable(Date) AS project_start_date,
        NULL::Nullable(Date) AS project_end_date,
        NULL::Nullable(Date) AS completion_date,
        NULL::Nullable(Date) AS cancellation_date,
        NULL::Nullable(Int128) AS percent_completed,
        NULLIFNEG(no_of_lands) AS no_of_lands,
        NULL::Nullable(Int128) AS no_of_buildings,
        NULL::Nullable(Int128) AS no_of_villas,
        NULL::Nullable(Int128) AS no_of_units,
        NULL::Nullable(Varchar) AS project_description_en,
        NULL::Nullable(Varchar) AS project_description_ar
    FROM (
        SELECT * FROM
        (
            SELECT
                MIN(area_id) OVER (PARTITION BY project_id) AS area_id,
                MIN(property_id) OVER (PARTITION BY project_id) AS property_id,
                MIN(NULLIFNEGS(master_project_id)) OVER (PARTITION BY project_id) AS master_project_id,
                LAST_VALUE(master_project_en) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_en,
                LAST_VALUE(master_project_ar) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_ar,
                project_id,
                project_id AS project_number,
                project_name_en,
                project_name_ar,
                COUNT(*) OVER (PARTITION BY project_id) - 1 AS no_of_lands
            FROM
                "{dld_database}"."{land_registry}_staging"
            WHERE project_id NOT IN (SELECT DISTINCT project_id FROM projects_clean_units)

        ) AS q0
        GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    ) AS q1
),
projects_land_existing AS
(
    SELECT
        area_id, 
        NULL::Nullable(Int128) AS zoning_authority_id,
        NULL::Nullable(Int128) AS master_developer_number,
        NULL::Nullable(Int128) AS developer_number,
        NULL::Nullable(Int128) AS escrow_agent_id,
        property_id,
        master_project_id,
        master_project_en,
        master_project_ar,
        project_id,
        project_id AS project_number,
        project_name_en,
        project_name_ar,
        NULL::Nullable(Int128) AS project_type_id,
        NULL::Nullable(Int128) AS project_classification_id,
        NULL::Nullable(Int128) AS project_status_id,
        NULL::Nullable(Date) AS project_start_date,
        NULL::Nullable(Date) AS project_end_date,
        NULL::Nullable(Date) AS completion_date,
        NULL::Nullable(Date) AS cancellation_date,
        NULL::Nullable(Int128) AS percent_completed,
        NULLIFNEG(no_of_lands) AS no_of_lands,
        NULL::Nullable(Int128) AS no_of_buildings,
        NULL::Nullable(Int128) AS no_of_villas,
        NULL::Nullable(Int128) AS no_of_units,
        NULL::Nullable(Varchar) AS project_description_en,
        NULL::Nullable(Varchar) AS project_description_ar
    FROM (
        SELECT * FROM
        (
            SELECT
                MIN(area_id) OVER (PARTITION BY project_id) AS area_id,
                MIN(property_id) OVER (PARTITION BY project_id) AS property_id,
                MIN(NULLIFNEGS(master_project_id)) OVER (PARTITION BY project_id) AS master_project_id,
                LAST_VALUE(master_project_en) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_en,
                LAST_VALUE(master_project_ar) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_ar,
                project_id,
                project_id AS project_number,
                project_name_en,
                project_name_ar,
                COUNT(*) OVER (PARTITION BY project_id) - 1 AS no_of_lands
            FROM
                "{dld_database}"."{land_registry}_staging"
            WHERE project_id IN (SELECT DISTINCT project_id FROM projects_clean_units)

        ) AS q0
        GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    ) AS q1
),
projects_clean_land_units AS
(
    SELECT 
        *
    FROM
    (
        SELECT 
            *
        FROM
        (
            SELECT 
                COALESCE(p0.area_id::Nullable(Int128), p1.area_id::Nullable(Int128)) AS area_id,
                COALESCE(p0.zoning_authority_id::Nullable(Int128), p1.zoning_authority_id::Nullable(Int128)) AS zoning_authority_id,
                COALESCE(p0.master_developer_number::Nullable(Int128), p1.master_developer_number::Nullable(Int128)) AS master_developer_number,
                COALESCE(p0.developer_number::Nullable(Int128), p1.developer_number::Nullable(Int128)) AS developer_number,
                COALESCE(p0.escrow_agent_id::Nullable(Int128), p1.escrow_agent_id::Nullable(Int128)) AS escrow_agent_id,
                COALESCE(p0.property_id::Nullable(Int128), p1.property_id::Nullable(Int128)) AS property_id,
                COALESCE(p0.master_project_id::Nullable(Int128), p1.master_project_id::Nullable(Int128)) AS master_project_id,
                COALESCE(p0.master_project_en,  p1.master_project_en) AS master_project_en,
                COALESCE(p0.master_project_ar, p1.master_project_ar) AS master_project_ar,
                COALESCE(p0.project_id::Nullable(Int128), p1.project_id::Nullable(Int128)) AS project_id,
                COALESCE(p0.project_number::Nullable(Int128), p1.project_number::Nullable(Int128)) AS project_number,
                COALESCE(p0.project_name_en, p1.project_name_en) AS project_name_en,
                COALESCE(p0.project_name_ar, p1.project_name_ar) AS project_name_ar,
                COALESCE(p0.project_type_id::Nullable(Int128), p1.project_type_id::Nullable(Int128)) AS project_type_id,
                COALESCE(p0.project_classification_id::Nullable(Int128), p1.project_classification_id::Nullable(Int128)) AS project_classification_id,
                COALESCE(p0.project_status_id::Nullable(Int128), p1.project_status_id::Nullable(Int128)) AS project_status_id,
                COALESCE(p0.project_start_date, p1.project_start_date) AS project_start_date,
                COALESCE(p0.project_end_date, p1.project_end_date) AS project_end_date,
                COALESCE(p0.completion_date, p1.completion_date) AS completion_date,
                COALESCE(p0.cancellation_date, p1.cancellation_date) AS cancellation_date,
                COALESCE(p0.percent_completed::Nullable(Int128), p1.percent_completed::Nullable(Int128)) AS percent_completed,
                COALESCE(p0.no_of_lands::Nullable(Int128), p1.no_of_lands::Nullable(Int128)) AS no_of_lands,
                COALESCE(p0.no_of_buildings::Nullable(Int128), p1.no_of_buildings::Nullable(Int128)) AS no_of_buildings,
                COALESCE(p0.no_of_villas::Nullable(Int128), p1.no_of_villas::Nullable(Int128)) AS no_of_villas,
                COALESCE(p0.no_of_units::Nullable(Int128), p1.no_of_units::Nullable(Int128)) AS no_of_units,
                COALESCE(p0.project_description_en, p1.project_description_en) AS project_description_en,
                COALESCE(p0.project_description_ar, p1.project_description_ar) AS project_description_ar
            FROM 
            projects_clean_units AS p0
            LEFT JOIN
            projects_land_existing AS p1
            USING(project_id)
        ) AS q0
        UNION ALL
        SELECT * FROM projects_land_missing
    ) AS q1
),
projects_buildings_missing AS
(
    SELECT
        area_id,
        NULL::Nullable(Int128) AS zoning_authority_id,
        NULL::Nullable(Int128) AS master_developer_number,
        NULL::Nullable(Int128) AS developer_number,
        NULL::Nullable(Int128) AS escrow_agent_id,
        NULL::Nullable(Int128) AS property_id,
        master_project_id,
        master_project_en,
        master_project_ar,
        project_id,
        project_number,
        project_name_en,
        project_name_ar,
        NULL::Nullable(Int128) AS project_type_id,
        NULL::Nullable(Int128) AS project_classification_id,
        NULL::Nullable(Int128) AS project_status_id,
        project_start_date,
        NULL::Nullable(Date) AS project_end_date,
        NULL::Nullable(Date) AS completion_date,
        NULL::Nullable(Date) AS cancellation_date,
        NULL::Nullable(Int128) AS percent_completed,
        NULL::Nullable(Int128) AS no_of_lands,
        no_of_buildings,
        no_of_villas,
        NULL::Nullable(Int128) AS no_of_units,
        NULL::Nullable(Varchar) AS project_description_en,
        NULL::Nullable(Varchar) AS project_description_ar
    FROM (
        SELECT * FROM
        (
            SELECT
                MIN(area_id) OVER (PARTITION BY project_id) AS area_id,
                MIN(NULLIFNEGS(master_project_id)) OVER (PARTITION BY project_id) AS master_project_id,
                LAST_VALUE(master_project_en) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_en,
                LAST_VALUE(master_project_ar) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_ar,
                project_id,
                project_id AS project_number,
                project_name_en,
                project_name_ar,
                MAX(creation_date) OVER (PARTITION BY project_id) AS project_start_date,
                SUM(CASE WHEN property_sub_type_id = 2 THEN 1 ELSE 0 END) OVER (PARTITION BY project_id) AS no_of_buildings,
                SUM(CASE WHEN property_sub_type_id = 4 THEN 1 ELSE 0 END) OVER (PARTITION BY project_id) AS no_of_villas
            FROM
                "{dld_database}"."{buildings}_staging"
            WHERE project_id NOT IN (SELECT DISTINCT project_id FROM projects_clean_land_units)
        ) AS q0
        GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    ) AS q1
),
projects_buildings_existing AS
(
    SELECT
        area_id,
        NULL::Nullable(Int128) AS zoning_authority_id,
        NULL::Nullable(Int128) AS master_developer_number,
        NULL::Nullable(Int128) AS developer_number,
        NULL::Nullable(Int128) AS escrow_agent_id,
        NULL::Nullable(Int128) AS property_id,
        master_project_id,
        master_project_en,
        master_project_ar,
        project_id,
        project_number,
        project_name_en,
        project_name_ar,
        NULL::Nullable(Int128) AS project_type_id,
        NULL::Nullable(Int128) AS project_classification_id,
        NULL::Nullable(Int128) AS project_status_id,
        project_start_date,
        NULL::Nullable(Date) AS project_end_date,
        NULL::Nullable(Date) AS completion_date,
        NULL::Nullable(Date) AS cancellation_date,
        NULL::Nullable(Int128) AS percent_completed,
        NULL::Nullable(Int128) AS no_of_lands,
        no_of_buildings,
        no_of_villas,
        NULL::Nullable(Int128) AS no_of_units,
        NULL::Nullable(Varchar) AS project_description_en,
        NULL::Nullable(Varchar) AS project_description_ar
    FROM (
        SELECT * FROM
        (
            SELECT
                MIN(area_id) OVER (PARTITION BY project_id) AS area_id,
                MIN(NULLIFNEGS(master_project_id)) OVER (PARTITION BY project_id) AS master_project_id,
                LAST_VALUE(master_project_en) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_en,
                LAST_VALUE(master_project_ar) IGNORE NULLS OVER (PARTITION BY project_id) AS master_project_ar,
                project_id,
                project_id AS project_number,
                project_name_en,
                project_name_ar,
                MAX(creation_date) OVER (PARTITION BY project_id) AS project_start_date,
                SUM(CASE WHEN property_sub_type_id = 2 THEN 1 ELSE 0 END) OVER (PARTITION BY project_id) AS no_of_buildings,
                SUM(CASE WHEN property_sub_type_id = 4 THEN 1 ELSE 0 END) OVER (PARTITION BY project_id) AS no_of_villas
            FROM
                "{dld_database}"."{buildings}_staging"
            WHERE project_id IN (SELECT DISTINCT project_id FROM projects_clean_land_units)

        ) AS q0
        GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    ) AS q1
),
projects_clean_land_buildings_units AS
(
    SELECT 
        *
    FROM
    (
        SELECT 
            *
        FROM
        (
            SELECT 
                COALESCE(p0.area_id::Nullable(Int128), p1.area_id::Nullable(Int128)) AS area_id,
                COALESCE(p0.zoning_authority_id::Nullable(Int128), p1.zoning_authority_id::Nullable(Int128)) AS zoning_authority_id,
                COALESCE(p0.master_developer_number::Nullable(Int128), p1.master_developer_number::Nullable(Int128)) AS master_developer_number,
                COALESCE(p0.developer_number::Nullable(Int128), p1.developer_number::Nullable(Int128)) AS developer_number,
                COALESCE(p0.escrow_agent_id::Nullable(Int128), p1.escrow_agent_id::Nullable(Int128)) AS escrow_agent_id,
                COALESCE(p0.property_id::Nullable(Int128), p1.property_id::Nullable(Int128)) AS property_id,
                COALESCE(p0.master_project_id::Nullable(Int128), p1.master_project_id::Nullable(Int128)) AS master_project_id,
                COALESCE(p0.master_project_en,  p1.master_project_en) AS master_project_en,
                COALESCE(p0.master_project_ar, p1.master_project_ar) AS master_project_ar,
                COALESCE(p0.project_id::Nullable(Int128), p1.project_id::Nullable(Int128)) AS project_id,
                COALESCE(p0.project_number::Nullable(Int128), p1.project_number::Nullable(Int128)) AS project_number,
                COALESCE(p0.project_name_en, p1.project_name_en) AS project_name_en,
                COALESCE(p0.project_name_ar, p1.project_name_ar) AS project_name_ar,
                COALESCE(p0.project_type_id::Nullable(Int128), p1.project_type_id::Nullable(Int128)) AS project_type_id,
                COALESCE(p0.project_classification_id::Nullable(Int128), p1.project_classification_id::Nullable(Int128)) AS project_classification_id,
                COALESCE(p0.project_status_id::Nullable(Int128), p1.project_status_id::Nullable(Int128)) AS project_status_id,
                COALESCE(p0.project_start_date, p1.project_start_date) AS project_start_date,
                COALESCE(p0.project_end_date, p1.project_end_date) AS project_end_date,
                COALESCE(p0.completion_date, p1.completion_date) AS completion_date,
                COALESCE(p0.cancellation_date, p1.cancellation_date) AS cancellation_date,
                COALESCE(p0.percent_completed::Nullable(Int128), p1.percent_completed::Nullable(Int128)) AS percent_completed,
                COALESCE(p0.no_of_lands::Nullable(Int128), p1.no_of_lands::Nullable(Int128)) AS no_of_lands,
                COALESCE(p0.no_of_buildings::Nullable(Int128), p1.no_of_buildings::Nullable(Int128)) AS no_of_buildings,
                COALESCE(p0.no_of_villas::Nullable(Int128), p1.no_of_villas::Nullable(Int128)) AS no_of_villas,
                COALESCE(p0.no_of_units::Nullable(Int128), p1.no_of_units::Nullable(Int128)) AS no_of_units,
                COALESCE(p0.project_description_en, p1.project_description_en) AS project_description_en,
                COALESCE(p0.project_description_ar, p1.project_description_ar) AS project_description_ar
            FROM 
            projects_clean_land_units AS p0
            LEFT JOIN
            projects_buildings_existing AS p1
            USING(project_id)
        ) AS q0
        UNION ALL
        SELECT * FROM projects_buildings_missing
    ) AS q1
),
projects_service_existing AS
(
    SELECT
        NULL::Nullable(Int128) AS area_id,
        NULL::Nullable(Int128) AS zoning_authority_id,
        NULL::Nullable(Int128) AS master_developer_number,
        NULL::Nullable(Int128) AS developer_number,
        NULL::Nullable(Int128) AS escrow_agent_id,
        NULL::Nullable(Int128) AS property_id,
        master_project_id,
        NULL::Nullable(Varchar) AS master_project_en,
        NULL::Nullable(Varchar) AS master_project_ar,
        project_id,
        project_id AS project_number,
        project_name_en,
        NULL::Nullable(Varchar) AS project_name_ar,
        NULL::Nullable(Int128) AS project_type_id,
        NULL::Nullable(Int128) AS project_classification_id,
        project_status_id,
        NULL::Nullable(Date) AS project_start_date,
        NULL::Nullable(Date) AS project_end_date,
        completion_date,
        NULL::Nullable(Date) AS cancellation_date,
        percent_completed,
        NULL::Nullable(Int128) AS no_of_lands,
        NULL::Nullable(Int128) AS no_of_buildings,
        NULL::Nullable(Int128) AS no_of_villas,
        NULL::Nullable(Int128) AS no_of_units,
        NULL::Nullable(Varchar) AS project_description_en,
        NULL::Nullable(Varchar) AS project_description_ar
    FROM (
        SELECT
            project_id,
            project_name AS project_name_en,
            MIN(NULLIFNEGS(master_community_id)) AS master_project_id,
            MIN((budget_year || '-01-01')::Nullable(Date)) AS completion_date,
            3 AS project_status_id,
            100 AS percent_completed
        FROM "{dld_database}"."{oa_service_charges}_staging"
        WHERE project_id > 0
        AND project_id IN (SELECT DISTINCT project_id FROM projects_clean_land_buildings_units)
        GROUP BY 1, 2
    ) AS q0
),
projects_service_missing AS
(
    SELECT
        NULL::Nullable(Int128) AS area_id,
        NULL::Nullable(Int128) AS zoning_authority_id,
        NULL::Nullable(Int128) AS master_developer_number,
        NULL::Nullable(Int128) AS developer_number,
        NULL::Nullable(Int128) AS escrow_agent_id,
        NULL::Nullable(Int128) AS property_id,
        master_project_id,
        NULL::Nullable(Varchar) AS master_project_en,
        NULL::Nullable(Varchar) AS master_project_ar,
        project_id,
        project_id AS project_number,
        project_name_en,
        NULL::Nullable(Varchar) AS project_name_ar,
        NULL::Nullable(Int128) AS project_type_id,
        NULL::Nullable(Int128) AS project_classification_id,
        project_status_id,
        NULL::Nullable(Date) AS project_start_date,
        NULL::Nullable(Date) AS project_end_date,
        completion_date,
        NULL::Nullable(Date) AS cancellation_date,
        percent_completed,
        NULL::Nullable(Int128) AS no_of_lands,
        NULL::Nullable(Int128) AS no_of_buildings,
        NULL::Nullable(Int128) AS no_of_villas,
        NULL::Nullable(Int128) AS no_of_units,
        NULL::Nullable(Varchar) AS project_description_en,
        NULL::Nullable(Varchar) AS project_description_ar
    FROM (
        SELECT
            project_id,
            project_name AS project_name_en,
            MIN(NULLIFNEGS(master_community_id)) AS master_project_id,
            MIN((budget_year || '-01-01')::Nullable(Date)) AS completion_date,
            3 AS project_status_id,
            100 AS percent_completed
        FROM "{dld_database}"."{oa_service_charges}_staging" 
        WHERE project_id > 0
        AND project_id NOT IN (SELECT DISTINCT project_id FROM projects_clean_land_buildings_units)
        GROUP BY 1, 2
    ) AS q0
),
projects_clean AS
(
    SELECT
        area_id,
        land_property_number,
        zoning_authority_id,
        master_developer_number,
        developer_number,
        escrow_agent_id,
        COALESCE(master_project_id, 
                 LAST_VALUE(master_project_id) IGNORE NULLS 
                            OVER (PARTITION BY master_project_en 
                                  ORDER BY cnt_master_project_en DESC),
                 project_id
                 ) AS master_project_id,
        master_project_en,
        master_project_ar,
        project_id,
        project_number,
        project_name_en,
        project_name_ar,
        project_type_id,
        project_classification_id,
        project_status_id,
        project_start_date,
        project_end_date,
        completion_date,
        cancellation_date,
        percent_completed,
        no_of_lands,
        no_of_buildings,
        no_of_villas,
        no_of_units,
        project_description_en,
        project_description_ar
    FROM
    (
        SELECT 
            area_id,
            property_id AS land_property_number,
            zoning_authority_id,
            master_developer_number,
            developer_number,
            escrow_agent_id,
            master_project_id,
            master_project_en,
            master_project_ar,
            project_id,
            project_number,
            project_name_en,
            project_name_ar,
            project_type_id,
            project_classification_id,
            project_status_id,
            project_start_date,
            project_end_date,
            completion_date,
            cancellation_date,
            percent_completed,
            no_of_lands,
            no_of_buildings,
            no_of_villas,
            no_of_units,
            project_description_en,
            project_description_ar,
            COUNT(*) OVER (PARTITION BY master_project_en) AS cnt_master_project_en
        FROM
        (
            SELECT 
                *
            FROM
            (
                SELECT 
                    COALESCE(p0.area_id::Nullable(Int128), p1.area_id::Nullable(Int128)) AS area_id,
                    COALESCE(p0.zoning_authority_id::Nullable(Int128), p1.zoning_authority_id::Nullable(Int128)) AS zoning_authority_id,
                    COALESCE(p0.master_developer_number::Nullable(Int128), p1.master_developer_number::Nullable(Int128)) AS master_developer_number,
                    COALESCE(p0.developer_number::Nullable(Int128), p1.developer_number::Nullable(Int128)) AS developer_number,
                    COALESCE(p0.escrow_agent_id::Nullable(Int128), p1.escrow_agent_id::Nullable(Int128)) AS escrow_agent_id,
                    COALESCE(p0.property_id::Nullable(Int128), p1.property_id::Nullable(Int128)) AS property_id,
                    COALESCE(p0.master_project_id::Nullable(Int128), p1.master_project_id::Nullable(Int128)) AS master_project_id,
                    COALESCE(p0.master_project_en,  p1.master_project_en) AS master_project_en,
                    COALESCE(p0.master_project_ar, p1.master_project_ar) AS master_project_ar,
                    COALESCE(p0.project_id::Nullable(Int128), p1.project_id::Nullable(Int128)) AS project_id,
                    COALESCE(p0.project_number::Nullable(Int128), p1.project_number::Nullable(Int128)) AS project_number,
                    COALESCE(p0.project_name_en, p1.project_name_en) AS project_name_en,
                    COALESCE(p0.project_name_ar, p1.project_name_ar) AS project_name_ar,
                    COALESCE(p0.project_type_id::Nullable(Int128), p1.project_type_id::Nullable(Int128)) AS project_type_id,
                    COALESCE(p0.project_classification_id::Nullable(Int128), p1.project_classification_id::Nullable(Int128)) AS project_classification_id,
                    COALESCE(p0.project_status_id::Nullable(Int128), p1.project_status_id::Nullable(Int128)) AS project_status_id,
                    COALESCE(p0.project_start_date, p1.project_start_date) AS project_start_date,
                    COALESCE(p0.project_end_date, p1.project_end_date) AS project_end_date,
                    COALESCE(p0.completion_date, p1.completion_date) AS completion_date,
                    COALESCE(p0.cancellation_date, p1.cancellation_date) AS cancellation_date,
                    COALESCE(p0.percent_completed::Nullable(Int128), p1.percent_completed::Nullable(Int128)) AS percent_completed,
                    COALESCE(p0.no_of_lands::Nullable(Int128), p1.no_of_lands::Nullable(Int128)) AS no_of_lands,
                    COALESCE(p0.no_of_buildings::Nullable(Int128), p1.no_of_buildings::Nullable(Int128)) AS no_of_buildings,
                    COALESCE(p0.no_of_villas::Nullable(Int128), p1.no_of_villas::Nullable(Int128)) AS no_of_villas,
                    COALESCE(p0.no_of_units::Nullable(Int128), p1.no_of_units::Nullable(Int128)) AS no_of_units,
                    COALESCE(p0.project_description_en, p1.project_description_en) AS project_description_en,
                    COALESCE(p0.project_description_ar, p1.project_description_ar) AS project_description_ar
                FROM 
                projects_clean_land_buildings_units AS p0
                LEFT JOIN
                projects_service_existing AS p1
                USING(project_id)
            ) AS q0
            UNION ALL
            SELECT * FROM projects_service_missing
        ) AS q1
    ) AS q2
)
SELECT 
    * 
FROM projects_clean;