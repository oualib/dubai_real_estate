CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    authority_id,
    participant_id,
    commerce_registry_number,
    chamber_commerce_number,
    rent_contract_no,
    parcel_id,
    main_office_id,
    MAP_LEGAL_TYPE_EN(legal_type_id) AS legal_type_english,
    MAP_LEGAL_TYPE_AR(legal_type_id) AS legal_type_arabic,
    MAP_ACTIVITY_TYPE_EN(activity_type_id) AS activity_type_english,
    MAP_ACTIVITY_TYPE_AR(activity_type_id) AS activity_type_arabic,
    MAP_STATUS_EN(status_id) AS status_english,
    MAP_STATUS_AR(status_id) AS status_arabic,
    license_number,
    license_issue_date,
    license_expiry_date,
    license_cancel_date,
    trade_name_en AS trade_name_english,
    trade_name_ar AS trade_name_arabic,
    print_rmker_ar AS print_rmker_arabic
FROM "{dld_database}"."{dld_table}_staging_clean"