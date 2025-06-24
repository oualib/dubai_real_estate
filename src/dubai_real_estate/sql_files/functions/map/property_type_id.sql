CREATE OR REPLACE FUNCTION MAP_PROPERTY_TYPE_EN AS (x) ->
    CASE 
        WHEN x = 1 THEN 'Land'
        WHEN x = 2 THEN 'Building'
        WHEN x = 3 THEN 'Unit'
        WHEN x = 4 THEN 'Villa'
    END;

CREATE OR REPLACE FUNCTION MAP_PROPERTY_TYPE_AR AS (x) ->
    CASE 
        WHEN x = 1 THEN 'ارض'
        WHEN x = 2 THEN 'مبنى'
        WHEN x = 3 THEN 'وحدة'
        WHEN x = 4 THEN 'فيلا'
    END;