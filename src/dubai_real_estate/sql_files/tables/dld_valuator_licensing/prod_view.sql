CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    valuation_company_number,
    valuation_company_name_en AS valuation_company_name_english,
    valuation_company_name_ar AS valuation_company_name_arabic,
    valuator_number,
    valuator_name_en AS valuator_name_english,
    valuator_name_ar AS valuator_name_arabic,
    license_start_date,
    license_end_date,
    MAP_NATIONALITY_EN(valuator_nationality_id) AS valuator_nationality_english,
    MAP_NATIONALITY_AR(valuator_nationality_id) AS valuator_nationality_arabic,
    is_female
FROM "{dld_database}"."{dld_table}_staging_clean"