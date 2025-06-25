CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    master_community_id,
    project_id,
    budget_year,
    usage_id,
    service_category_id,
    service_cost,
    property_group_id,
    property_group_name_en,
    property_group_name_ar,
    management_company_id,
    management_company_name_en,
    management_company_name_ar
FROM "{dld_database}"."{dld_table}_staging";