INSERT INTO "{dld_database}"."{dld_table}_staging"
SELECT 
	FORMAT_INT("escrow_agent_number") AS "escrow_agent_number",
	FORMAT_PHONE_NUMBER("phone") AS "phone"
FROM url(
    'https://www.dubaipulse.gov.ae/dataset/32281362-e4c7-41c6-97c2-8dca315cf9a3/resource/b1738b70-7a2b-4fe4-8295-2530bfcf9f42/download/accredited_escrow_agents.csv',
    'CSVWithNames'
);