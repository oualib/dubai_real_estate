CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT 
    authority_id,
    participant_id,
    commerce_registry_number,
    chamber_commerce_number,
    rent_contract_no,
    parcel_id,
    ded_activity_code AS main_office_id,
    legal_type_id,
    activity_type_id,
    status_id,
    license_number,
    issue_date AS license_issue_date,
    expiry_date AS license_expiry_date,
    cancel_date AS license_cancel_date,
    trade_name_en,
    trade_name_ar,
    print_rmker_ar
FROM "{dld_database}"."{dld_table}_staging";