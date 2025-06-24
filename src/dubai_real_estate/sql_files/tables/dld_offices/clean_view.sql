CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT
    real_estate_number,
    participant_id AS developer_participant_id,
    main_office_id,
    license_source_id,
    license_number,
    license_issue_date,
    license_expiry_date,
    is_branch,
    activity_type_id,
    contact_name_en,
    contact_name_ar,
    contact,
    phone,
    fax
FROM "{dld_database}"."{dld_table}_staging";