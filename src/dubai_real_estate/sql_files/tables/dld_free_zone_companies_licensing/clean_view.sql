CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    fz_company_number,
    fz_company_name_en,
    fz_company_name_ar,
    license_source_id,
    license_number,
    FORMAT_DATE_1(license_issue_date) AS license_issue_date,
    FORMAT_DATE_1(license_expiry_date) AS license_expiry_date,
    email,
    webpage,
    phone
FROM "{dld_database}"."{dld_table}_staging";