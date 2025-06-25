CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    real_estate_number,
    broker_id,
    license_start_date,
    license_end_date,
    broker_name_en AS broker_name_english,
    broker_name_ar AS broker_name_arabic,
    is_female,
	contact,
    phone
FROM "{dld_database}"."{dld_table}_staging_clean"