CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    parent_permit_id,
    MAP_SERVICE_EN(parent_service_id) AS parent_service_name_english,
    MAP_SERVICE_AR(parent_service_id) AS parent_service_name_arabic,
    permit_id,
    MAP_SERVICE_EN(service_id) AS service_name_english,
    MAP_SERVICE_AR(service_id) AS service_name_arabic,
    MAP_PERMIT_STATUS_EN(permit_status_id) AS permit_status_english,
    MAP_PERMIT_STATUS_AR(permit_status_id) AS permit_status_arabic,
    license_number,
    start_date,
    end_date,
    exhibition_name_en AS exhibition_name_english,
    exhibition_name_ar AS exhibition_name_arabic,
    participant_name_en AS participant_name_english,
    participant_name_ar AS participant_name_arabic,
    location
FROM "{dld_database}"."{dld_table}_staging_clean"