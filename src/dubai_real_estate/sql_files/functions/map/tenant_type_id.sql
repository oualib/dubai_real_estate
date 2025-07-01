CREATE OR REPLACE FUNCTION MAP_TENANT_TYPE_EN AS (x) ->
    CASE 
        WHEN x = 0 THEN 'Person'
        WHEN x = 1 THEN 'Authority'
    END;

CREATE OR REPLACE FUNCTION MAP_TENANT_TYPE_AR AS (x) ->
    CASE 
        WHEN x = 0 THEN 'شخص'
        WHEN x = 1 THEN 'جهة'
    END;