CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    real_estate_number,
    developer_participant_id,
    main_office_id,
    MAP_LICENSE_SOURCE_EN(license_source_id) AS license_source_name_english,
    MAP_LICENSE_SOURCE_AR(license_source_id) AS license_source_name_arabic,
    license_number,
    license_issue_date,
    license_expiry_date,
    is_branch,
    MAP_ACTIVITY_TYPE_EN(activity_type_id) AS activity_type_english,
    MAP_ACTIVITY_TYPE_AR(activity_type_id) AS activity_type_arabic,
    contact_name_en AS contact_name_english,
    contact_name_ar AS contact_name_arabic,
    contact,
    phone,
    fax
FROM "{dld_database}"."{dld_table}_staging_clean"