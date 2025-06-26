CREATE OR REPLACE VIEW 
"{dld_database}"."{dld_table}_staging_clean"
AS
SELECT 
    escrow_agent_id,
    MAX(phone) AS phone
FROM
(
    SELECT
        escrow_agent_number AS escrow_agent_id,
        phone
    FROM "{dld_database}"."{dld_table}_staging"
    UNION DISTINCT
    SELECT 
        escrow_agent_id,
        NULL 
    FROM "{dld_database}"."{projects}_staging"
    GROUP BY escrow_agent_id
) x
GROUP BY escrow_agent_id