CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    participant_id AS developer_participant_id,
    developer_number,
    developer_name_en,
    developer_name_ar,
    registration_date,
    chamber_commerce_number,
    legal_status AS legal_status_id,
    license_source_id,
    license_type_id,
    license_number,
    license_issue_date,
    license_expiry_date,
    contact,
    phone,
    fax
FROM "{dld_database}"."{dld_table}_staging";