CREATE OR REPLACE FUNCTION MAP_PROJECT_TYPE_EN AS (x) ->
    CASE 
        WHEN x = 1 THEN 'Normal'
        WHEN x = 2 THEN 'Infrastructure'
        WHEN x = 3 THEN 'Multiple'
    END;

CREATE OR REPLACE FUNCTION MAP_PROJECT_TYPE_AR AS (x) ->
    CASE 
        WHEN x = 1 THEN 'عادي'
        WHEN x = 2 THEN 'بنية تحتية'
        WHEN x = 3 THEN 'متعدد'
    END;