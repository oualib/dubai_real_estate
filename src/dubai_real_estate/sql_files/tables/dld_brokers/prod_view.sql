CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    real_estate_number,
    broker_name_en AS broker_name_english,
    broker_name_ar AS broker_name_arabic,
    license_start_date,
    license_end_date,
    is_female,
	contact,
    phone
FROM "{dld_database}"."{dld_table}_staging_clean"