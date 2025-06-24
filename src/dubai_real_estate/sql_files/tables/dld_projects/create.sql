CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"area_id" Integer,
		"zoning_authority_id" Nullable(Integer),
		"master_developer_id" Nullable(Integer),
		"master_developer_number" Nullable(Integer),
		"master_developer_name_ar" Nullable(Varchar(338)),
		"developer_number" Nullable(Integer),
		"developer_name_ar" Nullable(Varchar(338)),
		"escrow_agent_id" Nullable(Integer),
		"property_id" Nullable(Integer),
		"master_project_en" Nullable(Varchar(90)),
		"master_project_ar" Nullable(Varchar(150)),
		"project_id" Nullable(Integer),
		"project_number" Nullable(Integer),
		"project_name_ar" Nullable(Varchar(252)),
		"project_type_id" Nullable(Integer),
		"project_classification_id" Nullable(Integer),
		"project_status_en" Nullable(Varchar(44)),
		"project_start_date" Nullable(Date),
		"project_end_date" Nullable(Date),
		"completion_date" Nullable(Date),
		"cancellation_date" Nullable(Date),
		"percent_completed" Nullable(Integer),
		"no_of_lands" Nullable(Integer),
		"no_of_buildings" Nullable(Integer),
		"no_of_villas" Nullable(Integer),
		"no_of_units" Nullable(Integer),
		"project_description_en" Nullable(Varchar(2868)),
		"project_description_ar" Nullable(Varchar(4386))
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("area_id");