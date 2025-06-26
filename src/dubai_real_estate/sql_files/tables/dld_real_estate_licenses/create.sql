CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"authority_id" Nullable(Int128),
		"commerce_registry_number" Nullable(Varchar(100)),
		"chamber_commerce_number" Nullable(Int128),
		"ded_activity_code" Nullable(Int128),
		"parcel_id" Nullable(Int128),
		"rent_contract_no" Nullable(Varchar(100)),
		"participant_id" Int128,
		"license_number" Nullable(Varchar(100)),
		"status_id" Nullable(Int128),
		"issue_date" Nullable(Date),
		"expiry_date" Nullable(Date),
		"cancel_date" Nullable(Date),
		"legal_type_id" Nullable(Int128),
		"activity_type_id" Nullable(Int128),
		"trade_name_en" Nullable(Varchar(210)),
		"trade_name_ar" Nullable(Varchar(392)),
		"print_rmker_ar" Nullable(Varchar(316))
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("participant_id");