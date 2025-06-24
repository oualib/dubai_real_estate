CREATE OR REPLACE FUNCTION MAP_CONTRACT_REG_TYPE_EN AS (x) ->
    CASE 
        WHEN x = 1 THEN 'New'
        WHEN x = 2 THEN 'Renew'
    END;

CREATE OR REPLACE FUNCTION MAP_CONTRACT_REG_TYPE_AR AS (x) ->
    CASE 
        WHEN x = 1 THEN 'جديد'
        WHEN x = 2 THEN 'تجديد'
    END;