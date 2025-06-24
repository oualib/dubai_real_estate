CREATE OR REPLACE FUNCTION MAP_PROJECT_CLASSIFICATION_EN AS (x) ->
    CASE 
        WHEN x = 1 THEN 'Buildings'
        WHEN x = 2 THEN 'Villas'
        WHEN x = 3 THEN 'Villa Complex'
    END;

CREATE OR REPLACE FUNCTION MAP_PROJECT_CLASSIFICATION_AR AS (x) ->
    CASE 
        WHEN x = 1 THEN 'مباني'
        WHEN x = 2 THEN 'فلل'
        WHEN x = 3 THEN 'مجمع فلل'
    END;