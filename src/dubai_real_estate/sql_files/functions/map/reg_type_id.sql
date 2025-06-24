CREATE OR REPLACE FUNCTION MAP_REG_TYPE_EN AS (x) ->
    CASE 
        WHEN x = 0 THEN 'Off-Plan Properties'
        WHEN x = 1 THEN 'Existing Properties'
    END;

CREATE OR REPLACE FUNCTION MAP_REG_TYPE_AR AS (x) ->
    CASE 
        WHEN x = 0 THEN 'على الخارطة'
        WHEN x = 1 THEN 'العقارات القائمة'
    END;