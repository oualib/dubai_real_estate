CREATE OR REPLACE TABLE
"{dld_database}"."{dld_table}"(
        "escrow_agent_name_english" String COMMENT '[PK|JOIN] Escrow agent company name - joins to dld_projects.escrow_agent_name_english',
        "escrow_agent_name_arabic" Nullable(String) COMMENT '[NAME] Escrow agent company name in Arabic',
        "phone" Nullable(Int128) COMMENT '[CONTACT] Escrow agent contact phone number'
) 
ENGINE = MergeTree()
PRIMARY KEY("escrow_agent_name_english")
COMMENT 'Accredited escrow agents for real estate transactions';