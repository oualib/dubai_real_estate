CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    MAP_MASTER_COMMUNITY_EN(master_community_id) AS master_community_name_english,
    MAP_MASTER_COMMUNITY_AR(master_community_id) AS master_community_name_arabic,
    project_id,
    budget_year,
    MAP_USAGE_EN(usage_id) AS usage_type_english,
    MAP_USAGE_AR(usage_id) AS usage_type_arabic,
    MAP_SERVICE_CATEGORY_EN(service_category_id) AS service_category_type_english,
    MAP_SERVICE_CATEGORY_AR(service_category_id) AS service_category_type_arabic,
    service_cost AS service_cost_sqft,
    property_group_name_en AS property_group_name_english,
    property_group_name_ar AS property_group_name_arabic,
    management_company_name_en AS management_company_name_english,
    management_company_name_ar AS management_company_name_arabic
FROM "{dld_database}"."{dld_table}_staging_clean"