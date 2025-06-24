CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    company_name_en,
    company_name_ar,
    latitude,
    longitude,
    email,
    phone
FROM "{dld_database}"."{dld_table}_staging";