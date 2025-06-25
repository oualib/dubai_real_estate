CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    developer_participant_id,
    developer_number,
    developer_name_en AS developer_name_english,
    developer_name_ar AS developer_name_arabic,
    registration_date,
    chamber_commerce_number,
    MAP_LEGAL_STATUS_EN(legal_status_id) AS legal_status_type_english,
    MAP_LEGAL_STATUS_AR(legal_status_id) AS legal_status_type_arabic,
    MAP_LICENSE_SOURCE_DEV_EN(license_source_id) AS license_source_name_english,
    MAP_LICENSE_SOURCE_DEV_AR(license_source_id) AS license_source_name_arabic,
    MAP_LICENSE_TYPE_EN(license_type_id) AS license_type_english,
    MAP_LICENSE_TYPE_AR(license_type_id) AS license_type_arabic,
    license_number,
    license_issue_date,
    license_expiry_date,
    contact,
    phone,
    fax
FROM "{dld_database}"."{dld_table}_staging_clean"