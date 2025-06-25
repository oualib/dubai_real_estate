CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    parent_permit_id,
    parent_service_id,
    permit_id,
    service_id,
    permit_status_id,
    license_number,
    start_date,
    end_date,
    exhibition_name_en_final AS exhibition_name_en,
    exhibition_name_ar_final AS exhibition_name_ar,
    participant_name_en_final AS participant_name_en,
    participant_name_ar_final AS participant_name_ar,
    location
FROM
(
    SELECT
        parent_permit_id,
        parent_service_id,
        permit_id,
        service_id,
        permit_status_id,
        license_number,
        start_date,
        end_date,
        FIRST_EN(exhibition_name_en, exhibition_name_ar, NULL) AS exhibition_name_en_final,
        FIRST_AR(exhibition_name_ar, exhibition_name_en, NULL) AS exhibition_name_ar_final,
        FIRST_EN(participant_name_en, participant_name_ar, NULL) AS participant_name_en_final,
        FIRST_AR(participant_name_ar, participant_name_en, NULL) AS participant_name_ar_final,
        location
    FROM "{dld_database}"."{dld_table}_staging"
) dld_real_estate_permits_clean_view;