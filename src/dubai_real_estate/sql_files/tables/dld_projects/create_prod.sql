CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "area_name_english" Nullable(String) COMMENT '[GEO] Geographic area where project is located',
        "area_name_arabic" Nullable(String) COMMENT '[GEO] Geographic area in Arabic',
        "land_property_number" Nullable(Int128) COMMENT '[REF→dld_land_registry.land_property_number] Land property number where project is built',
        "zoning_authority_name_english" Nullable(String) COMMENT '[REF] Zoning authority responsible for the area (DEWA, Municipality, etc.)',
        "zoning_authority_name_arabic" Nullable(String) COMMENT '[REF] Zoning authority name in Arabic',
        "master_developer_number" Nullable(Int128) COMMENT '[FK] Master developer company identifier (for large communities)',
        "developer_number" Nullable(Int128) COMMENT '[FK→dld_developers.developer_number] Project developer company identifier',
        "escrow_agent_name_english" Nullable(String) COMMENT '[REF→dld_accredited_escrow_agents] Escrow agent handling project finances',
        "escrow_agent_name_arabic" Nullable(String) COMMENT '[REF] Escrow agent name in Arabic',
        "master_project_id" Nullable(Int128) COMMENT '[REF] Master project identifier for large communities',
        "master_project_english" Nullable(String) COMMENT '[REF] Master project name (e.g., Downtown Dubai, Business Bay, Palm Jumeirah)',
        "master_project_arabic" Nullable(String) COMMENT '[REF] Master project name in Arabic',
        "project_id" Nullable(Int128) COMMENT '[REF] Specific project identifier',
        "project_number" Int128 COMMENT '[PK] Unique project number assigned by DLD',
        "project_name_english" Nullable(String) COMMENT '[REF] Official project name (tower/building/community names)',
        "project_name_arabic" Nullable(String) COMMENT '[REF] Official project name in Arabic',
        "project_type_english" Nullable(String) COMMENT '[ENUM] Type of project (Residential|Commercial|Mixed|Industrial|etc.)',
        "project_type_arabic" Nullable(String) COMMENT '[ENUM] Type of project in Arabic',
        "project_classification_type_english" Nullable(String) COMMENT '[ENUM] Project classification category (varies by development scale)',
        "project_classification_type_arabic" Nullable(String) COMMENT '[ENUM] Project classification in Arabic',
        "project_status_english" Nullable(String) COMMENT '[ENUM] Project status: FINISHED (~45%), NOT STARTED (~25%), ACTIVE (~22%), PENDING (~8%)',
        "project_status_arabic" Nullable(String) COMMENT '[ENUM] Current project status in Arabic',
        "project_start_date" Nullable(Date) COMMENT '[DATE] Official project start date',
        "project_end_date" Nullable(Date) COMMENT '[DATE] Planned project completion date',
        "completion_date" Nullable(Date) COMMENT '[DATE] Actual project completion date (for FINISHED projects)',
        "cancellation_date" Nullable(Date) COMMENT '[DATE] Project cancellation date (if applicable)',
        "percent_completed" Nullable(Int128) COMMENT '[PERCENT] Project completion percentage (0-100)',
        "no_of_lands" Nullable(Int128) COMMENT '[COUNT] Number of land plots in project - Can be recomputed using joins and aggregations',
        "no_of_buildings" Nullable(Int128) COMMENT '[COUNT] Number of buildings in project - Can be recomputed using joins and aggregations',
        "no_of_villas" Nullable(Int128) COMMENT '[COUNT] Number of villa in project - Can be recomputed using joins and aggregations',
        "no_of_units" Nullable(Int128) COMMENT '[COUNT] Number of units in project - Can be recomputed using joins and aggregations',
        "project_description_english" Nullable(String) COMMENT '[TEXT] Detailed project description in English',
        "project_description_arabic" Nullable(String) COMMENT '[TEXT] Detailed project description in Arabic'
) 
ENGINE = MergeTree()
PRIMARY KEY("project_number")
COMMENT 'Real estate development projects and master communities with completion tracking';