CREATE OR REPLACE FUNCTION MAP_MARKET_TYPES_EN AS (x) ->
    CASE 
        WHEN x = 1 THEN 'Primary Market'
        WHEN x = 2 THEN 'Secondary Market'
    END;

CREATE OR REPLACE FUNCTION MAP_MARKET_TYPES_AR AS (x) ->
    CASE 
        WHEN x = 1 THEN 'السوق الأولي'
        WHEN x = 2 THEN 'السوق الثانوي'
    END;