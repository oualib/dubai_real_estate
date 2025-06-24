CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"contract_id" Nullable(Integer),
		"contract_type" Nullable(Varchar(8)),
		"area_id" Integer,
		"nearest_landmark_en" Nullable(Varchar(66)),
		"nearest_metro_en" Nullable(Varchar(72)),
		"nearest_mall_en" Nullable(Varchar(40)),
		"is_free_hold" Nullable(Bool),
		"property_type_id" Nullable(Integer),
		"master_project_en" Nullable(Varchar(90)),
		"master_project_ar" Nullable(Varchar(150)),
		"project_number" Nullable(Integer),
		"project_name_ar" Nullable(Varchar(252)),
		"project_name_en" Nullable(Varchar(154)),
		"tenant_type_id" Nullable(Integer),
		"contract_reg_type_id" Nullable(Integer),
		"contract_start_date" Nullable(Date),
		"contract_end_date" Nullable(Date),
		"ejari_property_type_id" Nullable(Integer),
		"no_of_prop" Nullable(Integer),
		"property_usage_en" Nullable(Varchar(74)),
		"rooms_en" Nullable(Varchar(54)),
		"actual_area" Nullable(Integer),
		"contract_amount" Nullable(Integer),
		"annual_amount" Nullable(Integer),
		"line_number" Nullable(Integer)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("area_id");