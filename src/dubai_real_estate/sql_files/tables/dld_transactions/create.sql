CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"transaction_id" Nullable(Varchar(34)),
		"trans_group_id" Nullable(Integer),
		"procedure_id" Nullable(Integer),
		"instance_date" Nullable(Date),
		"area_id" Integer,
		"nearest_landmark_en" Nullable(Varchar(66)),
		"nearest_metro_en" Nullable(Varchar(72)),
		"nearest_mall_en" Nullable(Varchar(40)),
		"property_type_id" Nullable(Integer),
		"property_sub_type_id" Nullable(Integer),
		"property_usage_en" Nullable(Varchar(48)),
		"reg_type_id" Nullable(Integer),
		"master_project_en" Nullable(Varchar(90)), 
		"master_project_ar" Nullable(Varchar(150)),
		"project_number" Nullable(Integer),
		"project_name_en" Nullable(Varchar(154)),
		"project_name_ar" Nullable(Varchar(252)),
		"building_name_en" Nullable(Varchar(148)),
		"building_name_ar" Nullable(Varchar(254)),
		"rooms_en" Nullable(Varchar(22)),
		"has_parking" Nullable(Bool),
		"procedure_area" Nullable(Float), 
		"actual_worth" Nullable(Float),
		"no_of_parties_role_1" Nullable(Integer),
		"no_of_parties_role_2" Nullable(Integer),
		"no_of_parties_role_3" Nullable(Integer)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("area_id");