CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"location" Nullable(Varchar(238)),
		"parent_permit_id" Nullable(Int128),
		"parent_service_id" Nullable(Int128),
		"permit_id" Int128,
		"service_id" Nullable(Int128),
		"permit_status_id" Nullable(Int128),
		"start_date" Nullable(Date),
		"end_date" Nullable(Date),
		"license_number" Nullable(Varchar(100)),
		"exhibition_name_en" Nullable(Varchar(104)),
		"exhibition_name_ar" Nullable(Varchar(156)),
		"participant_name_en" Nullable(Varchar(210)),
		"participant_name_ar" Nullable(Varchar(506))
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("permit_id");