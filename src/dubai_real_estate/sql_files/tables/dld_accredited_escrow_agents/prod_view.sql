CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_view"
AS
SELECT
    MAP_ESCROW_AGENT_EN(escrow_agent_id) AS escrow_agent_name_english,
    MAP_ESCROW_AGENT_AR(escrow_agent_id) AS escrow_agent_name_arabic,
    phone
FROM "{dld_database}"."{dld_table}_staging_clean"