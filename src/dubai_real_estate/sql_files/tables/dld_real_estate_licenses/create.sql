CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"authority_id" Nullable(Integer),
		"commerce_registry_number" Nullable(Varchar(100)),
		"chamber_commerce_number" Nullable(Integer),
		"ded_activity_code" Nullable(Integer),
		"parcel_id" Nullable(Integer),
		"rent_contract_no" Nullable(Varchar(100)),
		"participant_id" Integer,
		"license_number" Nullable(Varchar(100)),
		"status_id" Nullable(Varchar(100)),
		"issue_date" Nullable(Date),
		"expiry_date" Nullable(Date),
		"cancel_date" Nullable(Date),
		"legal_type_id" Nullable(Integer),
		"activity_type_id" Nullable(Integer),
		"trade_name_en" Nullable(Varchar(210)),
		"trade_name_ar" Nullable(Varchar(392)),
		"print_rmker_ar" Nullable(Varchar(316))
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("participant_id");