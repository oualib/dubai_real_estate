CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    real_estate_number,
    participant_id AS broker_id,
    CASE 
		WHEN 
			YEAR(license_start_date) > 1971 THEN license_start_date 
	END AS license_start_date,
    license_end_date,
    broker_name_en,
    broker_name_ar,
    is_female,
	contact,
    phone
FROM "{dld_database}"."{dld_table}_staging";