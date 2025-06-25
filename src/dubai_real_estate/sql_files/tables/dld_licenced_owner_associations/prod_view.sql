CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    company_name_en AS company_name_english,
    company_name_ar AS company_name_arabic,
    latitude,
    longitude,
    email,
    phone
FROM "{dld_database}"."{dld_table}_staging_clean"