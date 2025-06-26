CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"contract_id" Nullable(Varchar(26)),
		"area_id" Int128,
		"nearest_landmark_en" Nullable(Varchar(66)),
		"nearest_metro_en" Nullable(Varchar(72)),
		"nearest_mall_en" Nullable(Varchar(40)),
		"is_free_hold" Nullable(Bool),
		"property_type_id" Nullable(Int128),
		"master_project_en" Nullable(Varchar(90)),
		"master_project_ar" Nullable(Varchar(150)),
		"project_number" Nullable(Int128),
		"project_name_ar" Nullable(Varchar(252)),
		"project_name_en" Nullable(Varchar(154)),
		"tenant_type_id" Nullable(Int128),
		"contract_reg_type_id" Nullable(Int128),
		"contract_start_date" Nullable(Date),
		"contract_end_date" Nullable(Date),
		"ejari_property_type_id" Nullable(Int128),
		"no_of_prop" Nullable(Int128),
		"property_usage_en" Nullable(Varchar(74)),
		"rooms_en" Nullable(Varchar(54)),
		"actual_area" Nullable(Int128),
		"contract_amount" Nullable(Int128),
		"annual_amount" Nullable(Int128),
		"line_number" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("area_id");