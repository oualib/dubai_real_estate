CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}_staging"(
		"escrow_agent_number" Integer,
		"phone" Integer
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("escrow_agent_number");