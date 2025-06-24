CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    valuation_company_number,
    valuation_company_name_en,
    valuation_company_name_ar,
    valuator_number,
    valuator_name_en,
    valuator_name_ar,
    license_start_date,
    license_end_date,
    valuator_nationality_id,
    is_female
FROM "{dld_database}"."{dld_table}_staging";