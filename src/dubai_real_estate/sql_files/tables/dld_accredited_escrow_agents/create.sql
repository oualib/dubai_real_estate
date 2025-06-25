CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"escrow_agent_number" Int128,
		"phone" Int128
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("escrow_agent_number");