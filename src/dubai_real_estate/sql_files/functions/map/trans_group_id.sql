CREATE OR REPLACE FUNCTION MAP_TRANS_GROUP_EN AS (x) ->
    CASE 
        WHEN x = 1 THEN 'Sales'
        WHEN x = 2 THEN 'Mortgages'
        WHEN x = 3 THEN 'Gifts'
    END;

CREATE OR REPLACE FUNCTION MAP_TRANS_GROUP_AR AS (x) ->
    CASE 
        WHEN x = 1 THEN 'مبايعات'
        WHEN x = 2 THEN 'رهون'
        WHEN x = 3 THEN 'هبات'
    END;