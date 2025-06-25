CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    fz_company_number,
    fz_company_name_en AS fz_company_name_english,
    fz_company_name_ar AS fz_company_name_arabic,
    MAP_LICENSE_SOURCE_EN(license_source_id) AS license_source_name_english,
    MAP_LICENSE_SOURCE_AR(license_source_id) AS license_source_name_arabic,
    license_number,
    license_issue_date,
    license_expiry_date,
    email,
    webpage,
    phone
FROM "{dld_database}"."{dld_table}_staging_clean"