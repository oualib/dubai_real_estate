CREATE OR REPLACE TABLE
	"{dld_database}"."{dld_table}"(
        "escrow_agent_name_english" String,
        "escrow_agent_name_arabic" Nullable(String),
        "phone" Nullable(Int128)
	) 
    ENGINE = MergeTree()
    PRIMARY KEY("escrow_agent_name_english");